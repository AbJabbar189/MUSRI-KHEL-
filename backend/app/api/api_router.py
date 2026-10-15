from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.members import router as members_router
from app.api.cards import router as cards_router
from app.api.committees import router as committees_router
from app.api.professionals import router as professionals_router
from app.api.content import router as content_router
from app.api.finance import router as finance_router
from app.api.partners import router as partners_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)
api_router.include_router(members_router)
api_router.include_router(cards_router)
api_router.include_router(committees_router)
api_router.include_router(professionals_router)
api_router.include_router(content_router)
api_router.include_router(finance_router)
api_router.include_router(partners_router)
