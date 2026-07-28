"""
Main API v1 router — aggregates all endpoint modules.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, deals, documents, analysis, reports, dashboard

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(deals.router, prefix="/deals", tags=["Deals"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
