"""
Core PromptBuilder assembling provider-independent, optimized PromptResponse objects.
"""

import time
from typing import Dict, List, Type

from app.ai.prompting.guardrails import SafetyGuardrails
from app.ai.prompting.llm_profiles import get_llm_profile
from app.ai.prompting.output_schema_registry import OutputSchemaRegistry
from app.ai.prompting.personas import (
    AnalystPersona,
    BasePersona,
    InvestigatorPersona,
    LegalExpertPersona,
    SupervisorPersona,
)
from app.ai.prompting.plugins import CitationPlugin, HistoryPlugin, PromptPlugin
from app.ai.prompting.prompt_audit import PromptAuditEntry, PromptAuditTrail
from app.ai.prompting.prompt_cache import PromptCache
from app.ai.prompting.prompt_debug import PromptDebug, PromptTrace
from app.ai.prompting.prompt_metadata import PromptMetadataFactory
from app.ai.prompting.prompt_metrics import PromptMetrics
from app.ai.prompting.prompt_models import (
    PromptPersona,
    PromptRequest,
    PromptResponse,
)
from app.ai.prompting.prompt_optimizer import PromptOptimizer
from app.ai.prompting.prompt_quality import PromptQualityEvaluator
from app.ai.prompting.prompt_registry import PromptRegistry
from app.ai.prompting.prompt_sections import PromptSection
from app.ai.prompting.prompt_templates import TemplateEngine
from app.ai.prompting.prompt_validator import PromptValidator
from app.ai.prompting.prompt_variables import PromptVariables
from app.ai.prompting.token_budget_manager import TokenBudgetManager


class PromptBuilder:
    """
    Main builder class orchestrating template rendering, persona instructions,
    plugin execution, token budget allocation, prompt optimization, quality evaluation,
    and metadata creation.
    """

    _PERSONAS: Dict[PromptPersona, Type[BasePersona]] = {
        PromptPersona.INVESTIGATOR: InvestigatorPersona,
        PromptPersona.LEGAL_EXPERT: LegalExpertPersona,
        PromptPersona.ANALYST: AnalystPersona,
        PromptPersona.SUPERVISOR: SupervisorPersona,
    }

    def __init__(self, plugins: List[PromptPlugin] | None = None):
        self.plugins: List[PromptPlugin] = plugins if plugins is not None else [
            CitationPlugin(),
            HistoryPlugin(),
        ]

    def build(self, request: PromptRequest, use_cache: bool = True) -> PromptResponse:
        """
        Main pipeline building a complete PromptResponse for an input PromptRequest.
        """
        start_time = time.time()

        # 1. Check cache if enabled
        if use_cache:
            cached_resp = PromptCache.get(request)
            if cached_resp:
                return cached_resp

        trace_id = f"TRC-{PromptMetadataFactory.generate_prompt_id()}"
        trace = PromptTrace(trace_id=trace_id)
        trace.add_step("INIT", "Initialized prompt build pipeline", {"provider": request.provider_name})

        # 2. Plugin Hook: before_build
        for plugin in self.plugins:
            plugin.before_build(request)

        # 3. Resolve Persona & System Instructions
        persona_cls = self._PERSONAS.get(request.persona, InvestigatorPersona)
        persona_inst = persona_cls()
        system_instructions = persona_inst.get_system_instructions(request.profile)

        # 4. Resolve LLM Capability Profile & Provider Hints
        llm_prof = get_llm_profile(request.provider_name)
        effective_hints = llm_prof.get_provider_hints(request.provider_hints)

        # 5. Retrieve Template Asset & Manifest
        version_str = request.version or "1.0.0"
        template_raw, version_meta, template_name = PromptRegistry.get_template(
            request.prompt_type, version_str
        )
        trace.add_step("TEMPLATE_LOADED", f"Loaded template {template_name}", {"version": version_meta.version})

        # 6. Extract Context Sections & Apply Token Budget Allocation
        budget_map = TokenBudgetManager.allocate_budgets(request.max_token_budget or 4096)

        var_builder = PromptVariables(
            system_instructions=system_instructions,
            question=request.query or "Synthesize case context and provide comprehensive analysis.",
            guardrails=SafetyGuardrails.get_guardrails_text(),
            language=request.language,
            locale=request.locale,
        )

        # Apply output schema instructions if json format requested or available
        if request.output_format == "json" or llm_prof.supports_json:
            var_builder.output_instructions = OutputSchemaRegistry.get_formatting_instructions(request.prompt_type)

        # Populate context variables from RetrievalContext
        sections_used = []
        if request.retrieval_context:
            ctx_secs = request.retrieval_context.sections
            req_secs = [s.value for s in request.requested_sections] if request.requested_sections else None

            def should_include(sec_name: str) -> bool:
                return req_secs is None or sec_name in req_secs

            if should_include(PromptSection.SUMMARY.value) and ctx_secs.case_summary:
                var_builder.case_summary = "### CASE SUMMARY\n" + TokenBudgetManager.trim_to_budget(
                    ctx_secs.case_summary, budget_map["summary"]
                )
                sections_used.append("summary")

            if should_include(PromptSection.VICTIMS.value) and ctx_secs.victims:
                var_builder.victims = "### VICTIMS DETAILS\n" + TokenBudgetManager.trim_to_budget(
                    ctx_secs.victims, budget_map["victims"]
                )
                sections_used.append("victims")

            if should_include(PromptSection.ACCUSED.value) and ctx_secs.accused:
                var_builder.accused = "### ACCUSED DETAILS\n" + TokenBudgetManager.trim_to_budget(
                    ctx_secs.accused, budget_map["accused"]
                )
                sections_used.append("accused")

            if should_include(PromptSection.EVIDENCE.value) and ctx_secs.evidence:
                var_builder.evidence = "### EVIDENCE INVENTORY\n" + TokenBudgetManager.trim_to_budget(
                    ctx_secs.evidence, budget_map["evidence"]
                )
                sections_used.append("evidence")

            if should_include(PromptSection.TIMELINE.value) and ctx_secs.timeline:
                var_builder.timeline = "### CHRONOLOGICAL TIMELINE\n" + TokenBudgetManager.trim_to_budget(
                    ctx_secs.timeline, budget_map["timeline"]
                )
                sections_used.append("timeline")

            if should_include(PromptSection.LEGAL.value) and ctx_secs.legal:
                var_builder.legal = "### STATUTORY & LEGAL PROVISIONS\n" + TokenBudgetManager.trim_to_budget(
                    ctx_secs.legal, budget_map["legal"]
                )
                sections_used.append("legal")

        # 7. Plugin Hook: before_render
        for plugin in self.plugins:
            plugin.before_render(request, var_builder)

        # 8. Render Template
        rendered_user_prompt = TemplateEngine.render(template_raw, var_builder)
        trace.add_step("VARIABLES_INJECTED", "Rendered prompt template with variables")

        # 9. Plugin Hook: after_render
        for plugin in self.plugins:
            rendered_user_prompt = plugin.after_render(request, var_builder, rendered_user_prompt)

        # 10. Prompt Optimizer Stage
        opt_system_prompt, _, _ = PromptOptimizer.optimize(system_instructions)
        opt_user_prompt, orig_chars, opt_chars = PromptOptimizer.optimize(rendered_user_prompt)
        char_reduction = orig_chars - opt_chars
        trace.add_step("OPTIMIZER_APPLIED", f"Optimized prompt content ({char_reduction} chars reduced)")

        # 11. Plugin Hook: before_validate
        for plugin in self.plugins:
            opt_system_prompt, opt_user_prompt = plugin.before_validate(
                request, opt_system_prompt, opt_user_prompt
            )

        # 12. Validate Prompt
        PromptValidator.validate(
            system_prompt=opt_system_prompt,
            user_prompt=opt_user_prompt,
            max_budget=request.max_token_budget or 4096,
            raise_on_error=True,
        )
        trace.add_step("VALIDATOR_PASSED", "Validated prompt budget and placeholders")

        # 13. Estimate Tokens & Quality Score Evaluation
        full_prompt_text = opt_system_prompt + "\n" + opt_user_prompt
        est_tokens = TokenBudgetManager.estimate_tokens(full_prompt_text)

        quality_eval = PromptQualityEvaluator.evaluate(
            system_prompt=opt_system_prompt,
            user_prompt=opt_user_prompt,
            max_budget=request.max_token_budget or 4096,
            estimated_tokens=est_tokens,
            requested_sections=sections_used,
        )
        quality_score = quality_eval.get("quality_score", 100.0)

        # 14. Build Metadata, Audit Entry, and Debug Info
        prompt_id = PromptMetadataFactory.generate_prompt_id()
        metadata = PromptMetadataFactory.create_metadata(
            system_prompt=opt_system_prompt,
            user_prompt=opt_user_prompt,
            prompt_type=request.prompt_type,
            persona=request.persona,
            profile=request.profile,
            intent=request.intent,
            template_name=template_name,
            version=version_meta.version,
            estimated_tokens=est_tokens,
            quality_score=quality_score,
            provider_hints=effective_hints,
            prompt_id=prompt_id,
        )

        build_duration_ms = round((time.time() - start_time) * 1000, 2)

        debug_info = PromptDebug(
            template_name=template_name,
            template_version=version_meta.version,
            sections_used=sections_used,
            token_count_breakdown={
                "system": TokenBudgetManager.estimate_tokens(opt_system_prompt),
                "user": TokenBudgetManager.estimate_tokens(opt_user_prompt),
                "total": est_tokens,
            },
            context_hash=request.retrieval_context.provenance.context_hash if request.retrieval_context and request.retrieval_context.provenance else None,
            retrieval_id=request.retrieval_context.provenance.retrieval_id if request.retrieval_context and request.retrieval_context.provenance else None,
            placeholders_resolved=list(var_builder.to_dict().keys()),
            optimization_reduction_chars=char_reduction,
            build_time_ms=build_duration_ms,
        )

        # Construct final PromptResponse
        response = PromptResponse(
            system_prompt=opt_system_prompt,
            user_prompt=opt_user_prompt,
            metadata=metadata,
            debug=debug_info.model_dump(),
            trace=trace.model_dump(),
        )

        # 15. Plugin Hooks: after_validate & after_build
        for plugin in self.plugins:
            plugin.after_validate(request, response)
            plugin.after_build(request, response)

        # 16. Record Audit & Metrics
        PromptAuditTrail.record(
            PromptAuditEntry(
                prompt_id=metadata.prompt_id,
                prompt_fingerprint=metadata.prompt_fingerprint,
                template_name=template_name,
                version=version_meta.version,
                persona=request.persona.value,
                profile=request.profile.value,
                intent=request.intent.value,
                context_hash=debug_info.context_hash,
                retrieval_id=debug_info.retrieval_id,
                estimated_tokens=est_tokens,
                quality_score=quality_score,
            )
        )
        PromptMetrics.record_build(template_name, est_tokens)

        # 17. Store in Cache if enabled
        if use_cache:
            PromptCache.put(request, response)

        return response
