from typing import Annotated, List
from fastapi import Query
from pydantic import BaseModel, conint, constr
from uuid import UUID


class LibraryBase(BaseModel):
  name: Annotated[str, constr(max_length=80)]
  city: Annotated[str, constr(max_length=255)]
  address: Annotated[str, constr(max_length=255)]


class LibraryFilter(BaseModel):
  name: Annotated[str, Query(max_length=80)] | None = None
  city: Annotated[str, Query(max_length=255)] | None = None
  address: Annotated[str, Query(max_length=255)] | None = None
  

class LibraryUpdate(BaseModel):
  name: Annotated[str, constr(max_length=80)] | None = None
  city: Annotated[str, constr(max_length=255)] | None = None
  address: Annotated[str, constr(max_length=255)] | None = None


class LibraryCreate(LibraryBase):
  name: Annotated[str, constr(max_length=80)] | None = None
  city: Annotated[str, constr(max_length=255)] | None = None
  address: Annotated[str, constr(max_length=255)] | None = None


class Library(LibraryBase):
  id: int
  library_uid: UUID


class LibraryResponse(LibraryBase):
  library_uid: UUID


class LibraryPaginationResponse(BaseModel):
  page: Annotated[int, conint(ge=1)]
  pageSize: Annotated[int, conint(ge=1)]
  totalElements: Annotated[int, conint(ge=0)]
  items: List[LibraryResponse]
