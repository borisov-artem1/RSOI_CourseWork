from typing import Annotated, List
from pydantic import BaseModel, constr, conint, field_validator
from datetime import datetime
from uuid import UUID

from enums.status import ReservationStatus, ConditionStatus
from schemas.library import LibraryResponse, BookInfo
from schemas.rating import UserRatingResponse


def convert_datetime_to_iso_8601(dt: datetime) -> str:
  return dt.strftime('%Y-%m-%d')


class ReservationBase(BaseModel):
  username: Annotated[str, constr(max_length=80)]
  bookUid: UUID
  libraryUid: UUID
  status: ReservationStatus
  startDate: datetime
  tillDate: datetime

  @field_validator("startDate", "tillDate", mode="before")
  def datetime_validate(cls, dt):
    if dt:
      return datetime.fromisoformat(dt)


class Reservation(ReservationBase):
  reservationUid: UUID
  
class ReservationPaginationResponse(BaseModel):
  page: int
  pageSize: int
  totalElements: int
  items: List[Reservation]


class ReservationCreate(BaseModel):
  username: Annotated[str, constr(max_length=80)]
  library_uid: UUID | str
  book_uid: UUID | str
  status: ReservationStatus
  start_date: datetime | str
  till_date: datetime | str

  @field_validator("start_date", "till_date", mode="before")
  def datetime_validate(cls, dt):
    return datetime.fromisoformat(dt)
  

class ReservationUpdate(BaseModel):
  username: Annotated[str, constr(max_length=80)] | None = None
  library_uid: UUID | None = None
  book_uid: UUID | None = None
  status: ReservationStatus | None = None
  start_date: datetime | None = None
  till_date: datetime | None = None

  @field_validator("start_date", "till_date", mode="before")
  def datetime_validate(cls, dt):
    if dt:
      return datetime.fromisoformat(dt)


class BookReservationResponse(BaseModel):
  reservationUid: UUID
  username: Annotated[str, constr(max_length=80)]
  status: ReservationStatus
  startDate: datetime
  tillDate: datetime
  library: LibraryResponse
  book: BookInfo

  class Config:
    json_encoders = {
      datetime: convert_datetime_to_iso_8601
    }
    
class BookReservationPaginationResponse(BaseModel):
  page: int
  pageSize: int
  totalElements: int
  items: List[BookReservationResponse]


class TakeBookRequest(BaseModel):
  libraryUid: UUID
  bookUid: UUID
  tillDate: datetime

  @field_validator("tillDate", mode="before")
  def datetime_validate(cls, dt):
    if dt:
      return datetime.fromisoformat(dt)
    

class TakeBookResponse(BaseModel):
  reservationUid: UUID
  status: ReservationStatus
  startDate: datetime
  tillDate: datetime
  library: LibraryResponse
  book: BookInfo
  rating: UserRatingResponse

  class Config:
    json_encoders = {
      datetime: convert_datetime_to_iso_8601
    }


class ReturnBookRequest(BaseModel):
  condition: ConditionStatus
  date: datetime

  @field_validator("date", mode="before")
  def datetime_validate(cls, dt):
    if dt:
      return datetime.fromisoformat(dt)
