from fastapi import APIRouter, status
from fastapi.responses import Response

from schemas.api_response import ApiResponses
from enums.enums import DomainEnum


router = APIRouter(
  prefix="/manage",
  tags=["Manage"],
)


@router.get(
  "/health/",
  status_code=status.HTTP_200_OK,
  response_class=Response,
  responses={
      status.HTTP_200_OK: ApiResponses.health(DomainEnum.RATING),
  }
)
async def health():
  return Response(
    status_code=status.HTTP_200_OK
  )
