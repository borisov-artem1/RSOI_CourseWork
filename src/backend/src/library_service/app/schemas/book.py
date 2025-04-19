from typing import Annotated, List
from fastapi import Query
from pydantic import BaseModel, constr, conint
from uuid import UUID

from enums.status import ConditionStatus


class BookBase(BaseModel):
    name: Annotated[str, constr(max_length=255)]
    author: Annotated[str, constr(max_length=255)]
    genre: Annotated[str, constr(max_length=255)]
    condition: ConditionStatus


class BookFilter(BaseModel):
  name: Annotated[str | None, Query(max_length=255)] = None
  author: Annotated[str | None, Query(max_length=255)] = None
  genre: Annotated[str | None, Query(max_length=255)] = None
  condition: ConditionStatus | None = None
    

class BookUpdate(BaseModel):
    name: Annotated[str, constr(max_length=255)] | None = None
    author: Annotated[str, constr(max_length=255)] | None = None
    genre: Annotated[str, constr(max_length=255)] | None = None
    condition: ConditionStatus | None = None


class BookCreate(BookBase):
    condition: ConditionStatus = "EXCELLENT"


class Book(BookBase):
    id: int
    book_uid: UUID


class BookInfo(BookBase):
  book_uid: UUID


class BookPaginationResponse(BaseModel):
  page: Annotated[int, conint(ge=1)]
  pageSize: Annotated[int, conint(ge=1)]
  totalElements: Annotated[int, conint(ge=0)]
  items: List[BookInfo]
