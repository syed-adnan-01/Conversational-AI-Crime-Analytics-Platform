from fastapi import APIRouter
from importlib import import_module

from app.api.routes.auth import router as auth_router
from app.api.routes.cases import router as cases_router
from app.api.routes.complainants import router as complainants_router
from app.api.routes.victims import router as victims_router
from app.api.routes.accused import router as accused_router
from app.api.routes.acts import router as acts_router
from app.api.routes.sections import router as sections_router
from app.api.routes.case_sections import router as case_sections_router
from app.api.routes.evidence import router as evidence_router
from app.api.routes.timeline import router as timeline_router
from app.api.routes.witnesses import router as witnesses_router
from app.api.routes.arrests import router as arrests_router
from app.api.routes.officers import router as officers_router
from app.api.routes.chargesheets import router as chargesheets_router
from app.api.routes.court_proceedings import router as court_proceedings_router
from app.ai.routes.context import router as ai_context_router
from app.ai.routes.indexing import router as ai_indexing_router
from app.ai.routes.retrieval import router as ai_retrieval_router
from app.ai.routes.prompting import router as ai_prompting_router
from app.ai.routes.llm import router as ai_llm_router
from app.ai.routes.copilot import router as ai_copilot_router
from app.ai.routes.copilot_kb import router as ai_copilot_kb_router
from app.ai.routes.graph import router as ai_graph_router
from app.ai.routes.agents import router as ai_agents_router
from app.ai.routes.decision import router as ai_decision_router
from app.ai.evaluation.routes import router as ai_evaluation_router
from app.security.routes import router as security_router
from app.ai.governance.routes import router as ai_governance_router
from app.application.dashboard.routes import router as dashboard_router
from app.application.analytics.routes import router as application_analytics_router
from app.application.notifications.notification_router import router as application_notifications_router
from app.application.reports.routes import router as application_reports_router
from app.application.admin.routes import router as application_admin_router
from app.application.uploads.upload_router import router as application_uploads_router
ai_investigation_router = import_module("app.ai.routes.investigation").router
from app.api.routes.config import router as config_router
from app.api.routes.health import router as health_router
from app.api.routes.home import router as home_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.notifications import router as notifications_router
from app.api.routes.users import router as users_router


api_router = APIRouter()


# Home Routes
api_router.include_router(
    home_router,
    tags=["Home"],
)

# Health Routes
api_router.include_router(
    health_router,
    prefix="/health",
    tags=["Health"],
)

# Configuration Routes
api_router.include_router(
    config_router,
    prefix="/config",
    tags=["Configuration"],
)

api_router.include_router(users_router, prefix="/users", tags=["User Administration"])

# Authentication Routes
api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"],
)

# Case Management Routes
api_router.include_router(
    cases_router,
    prefix="/cases",
    tags=["Case Management"],
)

# Complainant Management Routes
api_router.include_router(
    complainants_router,
    tags=["Complainant Management"],
)

# Victim Management Routes
api_router.include_router(
    victims_router,
    tags=["Victim Management"],
)

# Accused Management Routes
api_router.include_router(
    accused_router,
    tags=["Accused Management"],
)

# Act & Section Management Routes
api_router.include_router(
    acts_router,
    tags=["Act & Section Management"],
)

api_router.include_router(
    sections_router,
    tags=["Act & Section Management"],
)

api_router.include_router(
    case_sections_router,
    tags=["Act & Section Management"],
)

# Evidence Management Routes
api_router.include_router(
    evidence_router,
    tags=["Evidence Management"],
)

# Investigation Timeline Routes
api_router.include_router(
    timeline_router,
    tags=["Investigation Timeline"],
)

# Witness Management Routes
api_router.include_router(
    witnesses_router,
    tags=["Witness Management"],
)

# Arrest Management Routes
api_router.include_router(
    arrests_router,
    tags=["Arrest Management"],
)

# Officer Master & Assignment Routes
api_router.include_router(
    officers_router,
    tags=["Officer Management"],
)

# Chargesheet Management Routes
api_router.include_router(
    chargesheets_router,
    tags=["Chargesheet Management"],
)

# Court Proceedings Routes
api_router.include_router(
    court_proceedings_router,
    tags=["Court Proceedings"],
)

# AI Context Builder Routes
api_router.include_router(
    ai_context_router,
    prefix="/ai/context",
    tags=["AI Context Builder"],
)

# AI Embedding & Vector Indexing Routes
api_router.include_router(
    ai_indexing_router,
    prefix="/ai/index",
    tags=["AI Vector Indexing"],
)

# AI RAG Retrieval Engine Routes
api_router.include_router(
    ai_retrieval_router,
    prefix="/ai/retrieve",
    tags=["AI RAG Retrieval"],
)

# AI Prompt Engine Routes
api_router.include_router(
    ai_prompting_router,
    prefix="/ai/prompt",
    tags=["AI Prompt Engine"],
)

# AI Enterprise LLM Gateway & Orchestrator Routes
api_router.include_router(
    ai_llm_router,
    prefix="/ai/llm",
    tags=["AI LLM Gateway"],
)

# AI Copilot & Conversation Intelligence Routes
api_router.include_router(
    ai_copilot_router,
    prefix="/ai/copilot",
    tags=["AI Copilot"],
)

api_router.include_router(
    ai_copilot_kb_router,
    prefix="/ai/copilot/kb",
    tags=["AI Copilot Knowledge Base"],
)

# AI Investigation Intelligence Routes
api_router.include_router(
    ai_investigation_router,
    prefix="/ai/investigation",
    tags=["AI Investigation Intelligence"],
)

# AI Crime Knowledge Graph Routes (additive, repository-backed)
api_router.include_router(
    ai_graph_router,
    prefix="/ai/graph",
    tags=["AI Crime Knowledge Graph"],
)

# AI Multi-Agent Investigation System Routes
api_router.include_router(
    ai_agents_router,
    prefix="/ai/agents",
    tags=["AI Multi-Agent Investigation"],
)

# AI Decision Intelligence & Explainable AI Routes
api_router.include_router(
    ai_decision_router,
    prefix="/ai/decision",
    tags=["AI Decision Intelligence"],
)

# AI Evaluation, Monitoring & Continuous Learning Routes
api_router.include_router(
    ai_evaluation_router,
    prefix="/ai/evaluation",
    tags=["AI Evaluation & Monitoring"],
)

# Enterprise Security and AI Governance routes
api_router.include_router(security_router, prefix="/security", tags=["Security"])
api_router.include_router(ai_governance_router, prefix="/ai/governance", tags=["AI Governance"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(application_analytics_router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(application_notifications_router, tags=["Notifications"])
api_router.include_router(application_reports_router, prefix="/reports", tags=["Reports"])
api_router.include_router(application_admin_router, prefix="/admin", tags=["Administration"])
api_router.include_router(application_uploads_router, tags=["Uploads"])
