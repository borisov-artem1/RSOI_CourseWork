from fastapi import APIRouter, status
from fastapi.responses import Response

from enums.enums import DomainEnum
from schemas.api_response import ApiResponses


router = APIRouter(
  prefix="/manage",
  tags=["Manage"],
)


@router.get(
  "/health/",
  status_code=status.HTTP_200_OK,
  response_class=Response,
  responses={
    status.HTTP_200_OK: ApiResponses.health(DomainEnum.STATISTICS),
  }
)
async def health():
  return Response(
    status_code=status.HTTP_200_OK
  )
