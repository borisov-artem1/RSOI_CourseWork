from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from schemas.response import CreatedResponse, NoContentResponse
from utils.auth_user import RoleChecker
from cruds.reservation import ReservationCRUD
from enums.enums import DomainEnum, RoleEnum
from schemas.api_response import ApiResponses
from schemas.reservation import Reservation, ReservationFilter, ReservationCreate, ReservationPaginationResponse, ReservationUpdate
from utils.database import get_db
from services.reservation import ReservationService
from enums.status import ReservationStatus


def get_reservation_crud() -> ReservationCRUD:
  return ReservationCRUD

def get_reservation_service(
  reservation_crud: Annotated[ReservationCRUD, Depends(get_reservation_crud)],
  db: Annotated[Session, Depends(get_db)],
) -> ReservationService:
  return ReservationService(
    reservationCRUD=reservation_crud,
    db=db,
  )

router = APIRouter(
  prefix="/reservation",
  tags=["Reservation REST API"],
  responses={
    status.HTTP_400_BAD_REQUEST: ApiResponses.invalid_data(DomainEnum.RESERVATION),
    status.HTTP_401_UNAUTHORIZED: ApiResponses.not_authorized(DomainEnum.RESERVATION),
    status.HTTP_403_FORBIDDEN: ApiResponses.forbidden(DomainEnum.RESERVATION),
  },
)


@router.get(
  path="/",
  status_code=status.HTTP_200_OK,
  response_model=ReservationPaginationResponse,
  responses={
    status.HTTP_200_OK: ApiResponses.get_all(DomainEnum.RESERVATION),
  }
)
async def get_all_reservation(
  reservation_service: Annotated[ReservationService, Depends(get_reservation_service)],
  filter: ReservationFilter = Depends(),
  page: Annotated[int, Query(ge=1)] = 1,
  size: Annotated[int, Query(ge=1)] = 100,
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  return await reservation_service.get_all(
      filter=filter,
      page=page,
      size=size,
    )


@router.get(
  path="/{uid}",
  status_code=status.HTTP_200_OK,
  response_model=Reservation,
  responses={
    status.HTTP_200_OK: ApiResponses.get_by_uuid(DomainEnum.RESERVATION),
    status.HTTP_404_NOT_FOUND: ApiResponses.not_found(DomainEnum.RESERVATION),
  },
)
async def get_reservation_by_uid(
  reservation_service: Annotated[ReservationService, Depends(get_reservation_service)],
  uid: UUID,
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  return await reservation_service.get_by_uid(
    uid=uid,
  )


@router.post(
  path="/",
  status_code=status.HTTP_201_CREATED,
  response_class=Response,
  responses={
    status.HTTP_201_CREATED: ApiResponses.create(DomainEnum.RESERVATION),
  },
)
async def create_reservation(
  reservation_service: Annotated[ReservationService, Depends(get_reservation_service)],
  reservation_create: ReservationCreate,
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  reservation = await reservation_service.create(
    reservation_create=reservation_create,
  )
  return CreatedResponse(
    domain=DomainEnum.RESERVATION,
    id=reservation.reservation_uid,
  )


@router.patch(
  path="/{uid}",
  status_code=status.HTTP_200_OK,
  response_model=Reservation,
  responses={
    status.HTTP_200_OK: ApiResponses.patch(DomainEnum.RESERVATION),
    status.HTTP_404_NOT_FOUND: ApiResponses.not_found(DomainEnum.RESERVATION),
  },
)
async def update_reservation(
  reservation_service: Annotated[ReservationService, Depends(get_reservation_service)],
  uid: UUID,
  reservation_update: ReservationUpdate,
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  return await reservation_service.patch(
    uid=uid,
    reservation_patch=reservation_update,
  )


@router.delete(
  path="/{uid}/",
  status_code=status.HTTP_204_NO_CONTENT,
  response_class=Response,
  responses={
    status.HTTP_204_NO_CONTENT: ApiResponses.delete(DomainEnum.RESERVATION),
    status.HTTP_404_NOT_FOUND: ApiResponses.not_found(DomainEnum.RESERVATION),
  },
)
async def delete_reservation(
  reservation_service: Annotated[ReservationService, Depends(get_reservation_service)],
  uid: UUID,
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  await reservation_service.delete(
    uid=uid,
  )
  return NoContentResponse()
