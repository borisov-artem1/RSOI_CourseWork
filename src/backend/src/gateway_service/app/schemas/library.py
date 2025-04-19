from typing import Annotated, List
from pydantic import BaseModel, conint, constr
from uuid import UUID

from enums.status import ConditionStatus


# ======= Library =======
class LibraryBase(BaseModel):
  name: Annotated[str, constr(max_length=80)] | None
  city: Annotated[str, constr(max_length=255)] | None
  address: Annotated[str, constr(max_length=255)] | None


class Library(LibraryBase):
  id: int
  library_uid: UUID


class LibraryResponse(LibraryBase):
  libraryUid: UUID | None


class LibraryPaginationResponse(BaseModel):
  page: int
  pageSize: int
  totalElements: int
  items: List[LibraryResponse]


# ======= Book =======
class BookBase(BaseModel):
  name: Annotated[str, constr(max_length=255)] | None
  author: Annotated[str, constr(max_length=255)] | None
  genre: Annotated[str, constr(max_length=255)] | None
  condition: ConditionStatus | None


class BookUpdate(BaseModel):
  name: Annotated[str, constr(max_length=255)] | None = None
  author: Annotated[str, constr(max_length=255)] | None = None
  genre: Annotated[str, constr(max_length=255)] | None = None
  condition: ConditionStatus | None = None


class Book(BookBase):
  id: int
  bookUid: UUID


class BookInfo(BookBase):
  bookUid: UUID | None


class BookPaginationResponse(BaseModel):
  page: Annotated[int, conint(ge=1)]
  pageSize: Annotated[int, conint(ge=1)]
  totalElements: Annotated[int, conint(ge=0)]
  items: List[BookInfo]


# ===== LibraryBookEntity =====
class LibraryBookEntityBase(BaseModel):
  libraryId: int
  bookId: int
  availableCount: int


class LibraryBookUpdate(BaseModel):
  library_id: Annotated[int, conint(ge=1)] | None = None
  book_id: Annotated[int, conint(ge=1)] | None = None
  available_count: Annotated[int, conint(ge=0)] | None = None


class LibraryBookEntity(LibraryBookEntityBase):
  id: int


class LibraryBookEntityResponse(LibraryBookEntityBase):
  id: int
  library: LibraryResponse
  book: BookInfo



# ===== LibraryBook =====
class LibraryBookResponse(BookBase):
  bookUid: UUID
  availableCount: int


class LibraryBookPaginationResponse(BaseModel):
  page: int
  pageSize: int
  totalElements: int
  items: List[LibraryBookResponse]
