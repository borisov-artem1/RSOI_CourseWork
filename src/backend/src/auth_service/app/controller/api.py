from fastapi import APIRouter

from controller import user

controller = APIRouter()
controller.include_router(user.controller)
