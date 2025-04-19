from fastapi import APIRouter

from routers import statistics, manage

router = APIRouter()
router.include_router(statistics.router)
router.include_router(manage.router)
