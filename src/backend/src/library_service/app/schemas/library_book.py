from typing import Annotated
from fastapi import Query
from pydantic import BaseModel, conint
from schemas.book import BookInfo
from schemas.library import LibraryResponse


class LibraryBookBase(BaseModel):
  library_id: int
  book_id: int
  available_count: int


class LibraryBookFilter(BaseModel):
  library_id: Annotated[int, Query(ge=1)] | None = None
  book_id: Annotated[int, Query(ge=1)] | None = None
  available_count: Annotated[int, Query(ge=1)] | None = None


class LibraryBookUpdate(BaseModel):
  library_id: Annotated[int, conint(ge=1)] | None = None
  book_id: Annotated[int, conint(ge=1)] | None = None
  available_count: Annotated[int, conint(ge=0)] | None = None


class LibraryBookCreate(LibraryBookBase):
  pass


class LibraryBook(LibraryBookBase):
  id: int


class LibraryBookResponse(LibraryBookBase):
  id: int
  library: LibraryResponse
  book: BookInfo


class LibraryBookPaginationResponse(BaseModel):
  page: Annotated[int, conint(ge=1)]
  pageSize: Annotated[int, conint(ge=1)]
  totalElements: Annotated[int, conint(ge=0)]
  items: list[LibraryBookResponse]
