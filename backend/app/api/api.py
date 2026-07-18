from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.cases import router as cases_router
from app.api.routes.complainants import router as complainants_router
from app.api.routes.victims import router as victims_router
from app.api.routes.accused import router as accused_router
from app.api.routes.acts import router as acts_router
from app.api.routes.sections import router as sections_router
from app.api.routes.case_sections import router as case_sections_router
from app.api.routes.evidence import router as evidence_router
from app.api.routes.config import router as config_router
from app.api.routes.health import router as health_router
from app.api.routes.home import router as home_router



api_router = APIRouter()

api_router.include_router(auth_router)

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

api_router.include_router(
    evidence_router,
    tags=["Evidence Management"],
)