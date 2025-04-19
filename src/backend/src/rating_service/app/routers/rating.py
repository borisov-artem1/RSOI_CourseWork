from typing import Annotated
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from utils.auth_user import RoleChecker
from cruds.rating import RatingCRUD
from enums.enums import DomainEnum, RoleEnum
from schemas.response import CreatedResponse, NoContentResponse
from schemas.api_response import ApiResponses
from schemas.rating import Rating, RatingFilter, RatingCreate, RatingUpdate
from utils.database import get_db
from services.rating import RatingService


def get_rating_crud() -> RatingCRUD:
  return RatingCRUD

def get_rating_service(
  rating_crud: Annotated[RatingCRUD, Depends(get_rating_crud)],
  db: Annotated[Session, Depends(get_db)],
) -> RatingService:
  return RatingService(
    ratingCRUD=rating_crud,
    db=db,
  )


router = APIRouter(
  prefix="/rating",
  tags=["Rating REST API"],
  responses={
    status.HTTP_400_BAD_REQUEST: ApiResponses.invalid_data(DomainEnum.RATING),
    status.HTTP_401_UNAUTHORIZED: ApiResponses.not_authorized(DomainEnum.RATING),
    status.HTTP_403_FORBIDDEN: ApiResponses.forbidden(DomainEnum.RATING),
  },
)


@router.get(
  path="/",
  status_code=status.HTTP_200_OK,
  response_model=list[Rating],
  responses={
    status.HTTP_200_OK: ApiResponses.get_all(DomainEnum.RATING),
  }
)
async def get_all_rating(
  rating_service: Annotated[RatingService, Depends(get_rating_service)],
  filter: RatingFilter = Depends(),
  page: Annotated[int, Query(ge=1)] = 1,
  size: Annotated[int, Query(ge=1)] = 100,
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  return await rating_service.get_all(
      filter=filter,
      page=page,
      size=size,
    )


@router.get(
  path="/{id}",
  status_code=status.HTTP_200_OK,
  response_model=Rating,
  responses={
    status.HTTP_200_OK: ApiResponses.get_by_uuid(DomainEnum.RATING),
    status.HTTP_404_NOT_FOUND: ApiResponses.not_found(DomainEnum.RATING),
  },
)
async def get_rating_by_id(
  rating_service: Annotated[RatingService, Depends(get_rating_service)],
  id: int,
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  return await rating_service.get_by_id(
    id=id,
  )


@router.post(
  path="/",
  status_code=status.HTTP_201_CREATED,
  response_class=Response,
  responses={
    status.HTTP_201_CREATED: ApiResponses.create(DomainEnum.RATING),
  },
)
async def create_rating(  
  rating_service: Annotated[RatingService, Depends(get_rating_service)],
  rating_create: RatingCreate,
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  rating = await rating_service.create(
    rating_create=rating_create,
  )
  return CreatedResponse(
    domain=DomainEnum.RATING,
    id = rating.id,
  )


@router.patch(
  path="/{id}",
  status_code=status.HTTP_200_OK,
  response_model=Rating,
  responses={
    status.HTTP_200_OK: ApiResponses.patch(DomainEnum.RATING),
    status.HTTP_404_NOT_FOUND: ApiResponses.not_found(DomainEnum.RATING),
  },
)
async def update_rating(  
  rating_service: Annotated[RatingService, Depends(get_rating_service)],
  id: int,
  rating_update: RatingUpdate,
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  return await rating_service.patch(
    id=id,
    rating_patch=rating_update,
  )


@router.delete(
  path="/{id}/",
  status_code=status.HTTP_204_NO_CONTENT,
  response_class=Response,
  responses={
    status.HTTP_204_NO_CONTENT: ApiResponses.delete(DomainEnum.RATING),
    status.HTTP_404_NOT_FOUND: ApiResponses.not_found(DomainEnum.RATING),
  },
)
async def delete_rating(
  rating_service: Annotated[RatingService, Depends(get_rating_service)],
  id: int,
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  await rating_service.delete(
    id=id,
  )
  return NoContentResponse()
