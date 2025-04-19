pass

from fastapi import APIRouter, status
from fastapi.responses import Response

from schemas.api_response import ApiResponses
from schemas.response import OkResponse
from enums.enums import DomainEnum


router = APIRouter(
  prefix="/manage",
  tags=["Manage"],
)


@router.get(
  path="/health/",
  status_code=status.HTTP_200_OK,
  response_class=Response,
  responses={
      status.HTTP_200_OK: ApiResponses.health(DomainEnum.LIBRARY),
  }
)
async def health():
  return OkResponse()
