"""
Central Prompt Registry managing template assets and JSON manifest metadata across versions.
"""

import json
from pathlib import Path
from typing import Dict, Optional, Tuple

from app.ai.prompting.exceptions import TemplateNotFoundException
from app.ai.prompting.prompt_models import PromptType, PromptVersion


class PromptRegistry:
    """
    Central registry mapping (PromptType, version) to template assets and JSON manifests.
    Templates are stored dynamically under app/ai/prompting/templates/<version>/<template>.md
    and manifest files under app/ai/prompting/templates/<version>/<template>.json
    """

    TEMPLATES_DIR = Path(__file__).parent / "templates"

    # Mapping of PromptType to template filename stem
    _TYPE_MAP: Dict[PromptType, str] = {
        PromptType.SUMMARY: "summary",
        PromptType.LEGAL_ANALYSIS: "legal",
        PromptType.CASE_ANALYSIS: "investigation",
        PromptType.TIMELINE: "timeline",
        PromptType.CHARGESHEET: "chargesheet",
        PromptType.REPORT: "report",
        PromptType.QUESTION_ANSWERING: "investigation",
        PromptType.NEXT_STEPS: "investigation",
        PromptType.EVIDENCE_ANALYSIS: "evidence",
    }

    @classmethod
    def get_template(
        cls, prompt_type: PromptType, version: str = "1.0.0"
    ) -> Tuple[str, PromptVersion, str]:
        """
        Loads template content and manifest metadata.
        Returns tuple: (template_content, prompt_version_metadata, template_name).
        """
        version_dir = f"v{version.split('.')[0]}" if not version.startswith("v") else version
        stem = cls._TYPE_MAP.get(prompt_type, "investigation")

        md_path = cls.TEMPLATES_DIR / version_dir / f"{stem}.md"
        json_path = cls.TEMPLATES_DIR / version_dir / f"{stem}.json"

        if not md_path.exists():
            # Fallback to v1 base template if specific version not found
            md_path = cls.TEMPLATES_DIR / "v1" / f"{stem}.md"
            json_path = cls.TEMPLATES_DIR / "v1" / f"{stem}.json"

        if not md_path.exists():
            raise TemplateNotFoundException(f"Template asset for '{prompt_type.value}' version '{version}' not found.")

        # Read Markdown template
        template_content = md_path.read_text(encoding="utf-8")

        # Read JSON manifest if present
        version_meta = PromptVersion(version=version)
        if json_path.exists():
            try:
                manifest_data = json.loads(json_path.read_text(encoding="utf-8"))
                version_meta = PromptVersion(
                    version=manifest_data.get("version", version),
                    supported_models=manifest_data.get(
                        "supported_models", ["gemini-2.5-pro", "gemini-2.5-flash", "quickml"]
                    ),
                    deprecated=manifest_data.get("deprecated", False),
                    description=manifest_data.get("description", "Standard template asset"),
                )
            except Exception:
                pass

        return template_content, version_meta, f"{stem}.md"

    @classmethod
    def list_templates(cls) -> list[dict[str, str]]:
        """Lists available template mappings."""
        return [
            {"prompt_type": p_type.value, "template_stem": stem}
            for p_type, stem in cls._TYPE_MAP.items()
        ]

    @classmethod
    def list_versions(cls) -> list[PromptVersion]:
        """Scans filesystem to return all available template versions."""
        versions = []
        if cls.TEMPLATES_DIR.exists():
            for v_dir in cls.TEMPLATES_DIR.iterdir():
                if v_dir.is_dir():
                    manifest_files = list(v_dir.glob("*.json"))
                    if manifest_files:
                        try:
                            m_data = json.loads(manifest_files[0].read_text(encoding="utf-8"))
                            versions.append(
                                PromptVersion(
                                    version=m_data.get("version", v_dir.name),
                                    supported_models=m_data.get("supported_models", []),
                                    deprecated=m_data.get("deprecated", False),
                                    description=m_data.get("description", f"Version {v_dir.name}"),
                                )
                            )
                        except Exception:
                            pass
        if not versions:
            versions.append(PromptVersion(version="1.0.0", description="v1 production assets"))
        return versions
