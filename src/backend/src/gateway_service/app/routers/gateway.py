from fastapi import APIRouter, Depends, status, Query, Header
from fastapi.responses import Response
from typing import Annotated
from uuid import UUID

from fastapi.security import HTTPAuthorizationCredentials

from enums.status import ReservationStatus
from schemas.user import UserPayloadDto
from utils.auth_user import RoleChecker, http_bearer, get_current_user
from enums.enums import RoleEnum
from schemas.api_response import GatewayApiResponses
from cruds.library import LibraryCRUD
from cruds.reservation import ReservationCRUD 
from cruds.rating import RatingCRUD
from schemas.library import (
  LibraryPaginationResponse,
  LibraryBookPaginationResponse,
)
from schemas.reservation import (
  BookReservationPaginationResponse,
  BookReservationResponse,
  TakeBookRequest,
  TakeBookResponse,
  ReturnBookRequest,
)
from schemas.rating import (
  UserRatingResponse,
)
from services.gateway import GatewayService


def get_library_crud() -> LibraryCRUD:
  return LibraryCRUD

def get_reservation_crud() -> ReservationCRUD:
  return ReservationCRUD

def get_rating_crud() -> RatingCRUD:
  return RatingCRUD

def get_gateway_service(
  libraryCRUD: Annotated[LibraryCRUD, Depends(get_library_crud)],
  reservationCRUD: Annotated[ReservationCRUD, Depends(get_reservation_crud)],
  ratingCRUD: Annotated[RatingCRUD, Depends(get_rating_crud)],
) -> GatewayService:
  return GatewayService(
    libraryCRUD=libraryCRUD,
    reservationCRUD=reservationCRUD,
    ratingCRUD=ratingCRUD,
  )


gateway_api_response = GatewayApiResponses()

router = APIRouter(
  tags=["Gateway API"],
  responses={
    status.HTTP_400_BAD_REQUEST: gateway_api_response.invalid_data(),
    status.HTTP_401_UNAUTHORIZED: gateway_api_response.not_authorized(),
    status.HTTP_403_FORBIDDEN: gateway_api_response.forbidden(),
  }
)


@router.get(
  path="/libraries", 
  status_code=status.HTTP_200_OK,
  response_model=LibraryPaginationResponse,
  responses={
    status.HTTP_200_OK: gateway_api_response.get_all_libraries_in_city(),
  }
)
async def get_all_libraries_in_city(
  gateway_service: Annotated[GatewayService, Depends(get_gateway_service)],
  city: Annotated[str, Query(max_length=80)] | None = None,
  page: Annotated[int, Query(ge=1)] = 1,
  size: Annotated[int, Query(ge=1)] = 100,
  # token: HTTPAuthorizationCredentials | None = Depends(http_bearer),
  # _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  return await gateway_service.get_all_libraries_in_city(
    city=city,
    page=page,
    size=size,
    # token=token,
  )


@router.get(
  path="/libraries/{libraryUid}/books",
  status_code=status.HTTP_200_OK,
  response_model=LibraryBookPaginationResponse,
  responses={
    status.HTTP_200_OK: gateway_api_response.get_all_books_in_library(),
  }
)
async def get_books_in_library(
  gateway_service: Annotated[GatewayService, Depends(get_gateway_service)],
  libraryUid: UUID,
  showAll: bool = False,
  page: Annotated[int, Query(ge=1)] = 1,
  size: Annotated[int, Query(ge=1)] = 100,
  # token: HTTPAuthorizationCredentials | None = Depends(http_bearer),
  # _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  return await gateway_service.get_books_in_library(
    library_uid=libraryUid,
    show_all=showAll,
    page=page,
    size=size,
    # token=token,
  )


@router.get(
  path="/reservations",
  status_code=status.HTTP_200_OK,
  response_model=BookReservationPaginationResponse,
  responses={
    status.HTTP_200_OK: gateway_api_response.get_user_rented_books(),
  },
)
async def get_user_rented_books(
  gateway_service: Annotated[GatewayService, Depends(get_gateway_service)],
  status: Annotated[ReservationStatus, Query()] | None = None,
  page: Annotated[int, Query(ge=1)] = 1,
  size: Annotated[int, Query(ge=1)] = 100,
  token: HTTPAuthorizationCredentials | None = Depends(http_bearer),
  user: UserPayloadDto = Depends(get_current_user),
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  return await gateway_service.get_user_rented_books(
    X_User_Name=user.login,
    status=status,
    page=page,
    size=size,
    token=token,
  )


@router.get(
  path="/rating",
  status_code=status.HTTP_200_OK,
  response_model=UserRatingResponse,
  responses={
    status.HTTP_200_OK: gateway_api_response.get_user_rating(),
  }
)
async def get_user_rating(
  gateway_service: Annotated[GatewayService, Depends(get_gateway_service)],
  token: HTTPAuthorizationCredentials | None = Depends(http_bearer),
  user: UserPayloadDto = Depends(get_current_user),
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  return await gateway_service.get_user_rating(
    X_User_Name=user.login,
    token=token,
  )


@router.post(
  path="/reservations",
  status_code=status.HTTP_200_OK,
  response_model=TakeBookResponse,
  responses={
    status.HTTP_200_OK: gateway_api_response.take_book(),
  }
)
async def take_book(
  gateway_service: Annotated[GatewayService, Depends(get_gateway_service)],
  take_book_request: TakeBookRequest,
  token: HTTPAuthorizationCredentials | None = Depends(http_bearer),
  user: UserPayloadDto = Depends(get_current_user),
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  return await gateway_service.take_book(
    X_User_Name=user.login,
    take_book_request=take_book_request,
    token=token,
  )


@router.post(
  path="/reservations/{reservationUid}/return",
  status_code=status.HTTP_204_NO_CONTENT,
  response_model=None,
  responses={
    status.HTTP_204_NO_CONTENT: gateway_api_response.return_book(),
    status.HTTP_404_NOT_FOUND: gateway_api_response.reservation_not_found(),
  }
)
async def return_book(
  gateway_service: Annotated[GatewayService, Depends(get_gateway_service)],
  reservationUid: UUID,
  return_book_request: ReturnBookRequest,
  token: HTTPAuthorizationCredentials | None = Depends(http_bearer),
  user: UserPayloadDto = Depends(get_current_user),
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  return await gateway_service.return_book(
    X_User_Name=user.login,
    reservation_uid=reservationUid,
    return_book_request=return_book_request,
    token=token,
  )
