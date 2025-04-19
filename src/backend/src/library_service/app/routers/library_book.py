from typing import Annotated
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from utils.auth_user import RoleChecker
from cruds.library_book import LibraryBookCRUD
from schemas.api_response import ApiResponses
from schemas.response import CreatedResponse, NoContentResponse
from enums.enums import RoleEnum, DomainEnum
from schemas.library_book import LibraryBook, LibraryBookFilter, LibraryBookCreate, LibraryBookUpdate, LibraryBookPaginationResponse
from utils.database import get_db
from services.library_book import LibraryBookService


def get_library_book_crud() -> LibraryBookCRUD:
  return LibraryBookCRUD

def get_library_book_service(
  library_book_crud: Annotated[LibraryBook, Depends(get_library_book_crud)],
  db: Annotated[Session, Depends(get_db)],
) -> LibraryBookService:
  return LibraryBookService(
    library_bookCRUD=library_book_crud,
    db=db,
  )


router = APIRouter(
  prefix="/library_book",
  tags=["LibraryBook REST API"],
  responses={
    status.HTTP_400_BAD_REQUEST: ApiResponses.invalid_data(DomainEnum.LIBRARY_BOOK),
    status.HTTP_401_UNAUTHORIZED: ApiResponses.not_authorized(DomainEnum.LIBRARY_BOOK),
    status.HTTP_403_FORBIDDEN: ApiResponses.forbidden(DomainEnum.LIBRARY_BOOK),
  },
)


@router.get(
  path="/",
  status_code=status.HTTP_200_OK,
  response_model=LibraryBookPaginationResponse,
  responses={
    status.HTTP_200_OK: ApiResponses.get_all(DomainEnum.LIBRARY_BOOK),
  }
)
async def get_all_library_book(
  library_book_service: Annotated[LibraryBookService, Depends(get_library_book_service)],
  filter: LibraryBookFilter = Depends(),
  page: Annotated[int, Query(ge=1)] = 1,
  size: Annotated[int, Query(ge=1)] = 100,
  # _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  return await library_book_service.get_all(
      filter=filter,
      page=page,
      size=size,
    )


@router.get(
  path="/{id}",
  status_code=status.HTTP_200_OK,
  response_model=LibraryBook,
  responses={
    status.HTTP_200_OK: ApiResponses.get_by_uuid(DomainEnum.LIBRARY_BOOK),
    status.HTTP_404_NOT_FOUND: ApiResponses.not_found(DomainEnum.LIBRARY_BOOK),
  },
)
async def get_library_book_by_id(
  library_book_service: Annotated[LibraryBookService, Depends(get_library_book_service)],
  id: int,
  # _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  return await library_book_service.get_by_id(
    id=id,
  )


@router.post(
  path="/",
  status_code=status.HTTP_201_CREATED,
  response_class=Response,
  responses={
    status.HTTP_201_CREATED: ApiResponses.create(DomainEnum.LIBRARY_BOOK),
  },
)
async def create_library_book(
  library_book_service: Annotated[LibraryBookService, Depends(get_library_book_service)],
  library_book_create: LibraryBookCreate,
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.MODERATOR])),
):
  library_book = await library_book_service.create(
    library_book_create=library_book_create,
  )
  return CreatedResponse(
    domain=DomainEnum.LIBRARY_BOOK,
    id=library_book.id,
  )


@router.patch(
  path="/{id}",
  status_code=status.HTTP_200_OK,
  response_model=LibraryBook,
  responses={
    status.HTTP_200_OK: ApiResponses.patch(DomainEnum.LIBRARY_BOOK),
    status.HTTP_404_NOT_FOUND: ApiResponses.not_found(DomainEnum.LIBRARY_BOOK),
  },
)
async def update_library_book(
  library_book_service: Annotated[LibraryBookService, Depends(get_library_book_service)],
  id: int,
  library_book_update: LibraryBookUpdate,
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  return await library_book_service.patch(
    id=id,
    library_book_patch=library_book_update,
  )


@router.delete(
  path="/{id}/",
  status_code=status.HTTP_204_NO_CONTENT,
  response_class=Response,
  responses={
    status.HTTP_204_NO_CONTENT: ApiResponses.delete(DomainEnum.LIBRARY_BOOK),
    status.HTTP_404_NOT_FOUND: ApiResponses.not_found(DomainEnum.LIBRARY_BOOK),
  },
)
async def delete_library_book(
  library_book_service: Annotated[LibraryBookService, Depends(get_library_book_service)],
  id: int,
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.MODERATOR])),
):
  await library_book_service.delete(
    id=id,
  )
  return NoContentResponse()
