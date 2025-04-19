from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from utils.auth_user import RoleChecker
from cruds.book import BookCRUD
from schemas.api_response import ApiResponses
from schemas.response import CreatedResponse, NoContentResponse
from enums.enums import RoleEnum, DomainEnum
from schemas.book import Book, BookFilter, BookCreate, BookUpdate
from utils.database import get_db
from services.book import BookService


def get_book_crud() -> BookCRUD:
  return BookCRUD

def get_book_service(
  book_crud: Annotated[BookCRUD, Depends(get_book_crud)],
  db: Annotated[Session, Depends(get_db)],
) -> BookService:
  return BookService(
    bookCRUD=book_crud,
    db=db,
  )


router = APIRouter(
  prefix="/book",
  tags=["Book REST API"],
  responses={
    status.HTTP_400_BAD_REQUEST: ApiResponses.invalid_data(DomainEnum.BOOK),
    status.HTTP_401_UNAUTHORIZED: ApiResponses.not_authorized(DomainEnum.BOOK),
    status.HTTP_403_FORBIDDEN: ApiResponses.forbidden(DomainEnum.BOOK),
  },
)


@router.get(
  path="/",
  status_code=status.HTTP_200_OK,
  response_model=list[Book],
  responses={
    status.HTTP_200_OK: ApiResponses.get_all(DomainEnum.BOOK),
  }
)
async def get_all_book(
  book_service: Annotated[BookService, Depends(get_book_service)],
  filter: BookFilter = Depends(),
  page: Annotated[int, Query(ge=1)] = 1,
  size: Annotated[int, Query(ge=1)] = 100,
  # _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  return await book_service.get_all(
      filter=filter,
      page=page,
      size=size,
    )


@router.get(
  path="/{uid}",
  status_code=status.HTTP_200_OK,
  response_model=Book,
  responses={
    status.HTTP_200_OK: ApiResponses.get_by_uuid(DomainEnum.BOOK),
    status.HTTP_404_NOT_FOUND: ApiResponses.not_found(DomainEnum.BOOK),
  },
)
async def get_book_by_uid(
  book_service: Annotated[BookService, Depends(get_book_service)],
  uid: UUID,
  # _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  return await book_service.get_by_uid(
    uid=uid,
  )


@router.post(
  path="/",
  status_code=status.HTTP_201_CREATED,
  response_class=Response,
  responses={
    status.HTTP_201_CREATED: ApiResponses.create(DomainEnum.BOOK),
  },
)
async def create_book(
  book_service: Annotated[BookService, Depends(get_book_service)],
  book_create: BookCreate,
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.MODERATOR])),
):
  book = await book_service.create(
    book_create=book_create,
  )
  return CreatedResponse(
    domain=DomainEnum.BOOK,
    id=book.book_uid,
  )


@router.patch(
  path="/{uid}",
  status_code=status.HTTP_200_OK,
  response_model=Book,
  responses={
    status.HTTP_200_OK: ApiResponses.patch(DomainEnum.BOOK),
    status.HTTP_404_NOT_FOUND: ApiResponses.not_found(DomainEnum.BOOK),
  },
)
async def update_book(
  book_service: Annotated[BookService, Depends(get_book_service)],
  uid: UUID,
  book_update: BookUpdate,
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.USER, RoleEnum.MODERATOR])),
):
  return await book_service.patch(
    uid=uid,
    book_patch=book_update,
  )


@router.delete(
  path="/{uid}/",
  status_code=status.HTTP_204_NO_CONTENT,
  response_class=Response,
  responses={
    status.HTTP_204_NO_CONTENT: ApiResponses.delete(DomainEnum.BOOK),
    status.HTTP_404_NOT_FOUND: ApiResponses.not_found(DomainEnum.BOOK),
  },
)
async def delete_book(
  book_service: Annotated[BookService, Depends(get_book_service)],
  uid: UUID,
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.MODERATOR])),
):
  await book_service.delete(
    uid=uid,
  )
  return NoContentResponse()
