from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from enums.enums import DomainEnum, RoleEnum
from utils.auth_user import RoleChecker
from cruds.library import LibraryCRUD
from schemas.api_response import ApiResponses
from schemas.response import CreatedResponse, NoContentResponse
from schemas.library import Library, LibraryFilter, LibraryCreate, LibraryUpdate, LibraryPaginationResponse
from utils.database import get_db
from services.library import LibraryService


def get_library_crud() -> LibraryCRUD:
  return LibraryCRUD

def get_library_service(
  library_crud: Annotated[LibraryCRUD, Depends(get_library_crud)],
  db: Annotated[Session, Depends(get_db)],
) -> LibraryService:
  return LibraryService(
    libraryCRUD=library_crud,
    db=db,
  )

router = APIRouter(
  prefix="/library",
  tags=["Library REST API"],
  responses={
    status.HTTP_400_BAD_REQUEST: ApiResponses.invalid_data(DomainEnum.LIBRARY),
    status.HTTP_401_UNAUTHORIZED: ApiResponses.not_authorized(DomainEnum.LIBRARY),
    status.HTTP_403_FORBIDDEN: ApiResponses.forbidden(DomainEnum.LIBRARY),
  },
)

@router.get(
  path="/",
  status_code=status.HTTP_200_OK,
  response_model=LibraryPaginationResponse,
  responses={
    status.HTTP_200_OK: ApiResponses.get_all(DomainEnum.LIBRARY),
  }
)
async def get_all_library(
  library_service: Annotated[LibraryService, Depends(get_library_service)],
  filter: LibraryFilter = Depends(),
  page: Annotated[int, Query(ge=1)] = 1,
  size: Annotated[int, Query(ge=1)] = 100,
  # _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  return await library_service.get_all(
    filter=filter,
    page=page,
    size=size,
  )


@router.get(
  path="/{uid}",
  status_code=status.HTTP_200_OK,
  response_model=Library,
  responses={
    status.HTTP_200_OK: ApiResponses.get_by_uuid(DomainEnum.LIBRARY),
    status.HTTP_404_NOT_FOUND: ApiResponses.not_found(DomainEnum.LIBRARY),
  },
)
async def get_library_by_uid(
  library_service: Annotated[LibraryService, Depends(get_library_service)],
  uid: UUID,
  # _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  return await library_service.get_by_uid(
    uid=uid,
  )


@router.post(
  path="/",
  status_code=status.HTTP_201_CREATED,
  response_class=Response,
  responses={
    status.HTTP_201_CREATED: ApiResponses.create(DomainEnum.LIBRARY),
  },
)
async def create_library(
  library_service: Annotated[LibraryService, Depends(get_library_service)],
  library_create: LibraryCreate,
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.MODERATOR])),
):
  library = await library_service.create(
    library_create=library_create,
  )
  return CreatedResponse(
    domain=DomainEnum.LIBRARY,
    id=library.library_uid,
  )


@router.patch(
  path="/{uid}",
  status_code=status.HTTP_200_OK,
  response_model=Library,
  responses={
    status.HTTP_200_OK: ApiResponses.patch(DomainEnum.LIBRARY),
    status.HTTP_404_NOT_FOUND: ApiResponses.not_found(DomainEnum.LIBRARY),
  },
)
async def update_library(
  library_service: Annotated[LibraryService, Depends(get_library_service)],
  uid: UUID,
  library_update: LibraryUpdate,
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.MODERATOR])),
):
  return await library_service.patch(
    uid=uid,
    library_patch=library_update,
  )


@router.delete(
  path="/{uid}/",
  status_code=status.HTTP_204_NO_CONTENT,
  response_class=Response,
  responses={
    status.HTTP_204_NO_CONTENT: ApiResponses.delete(DomainEnum.LIBRARY),
    status.HTTP_404_NOT_FOUND: ApiResponses.not_found(DomainEnum.LIBRARY),
  },
)
async def delete_library(
  library_service: Annotated[LibraryService, Depends(get_library_service)],
  uid: UUID,
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.MODERATOR])),
):
  await library_service.delete(
    uid=uid,
  )
  return NoContentResponse()
