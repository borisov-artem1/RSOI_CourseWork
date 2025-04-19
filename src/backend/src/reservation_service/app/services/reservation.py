from uuid import UUID
from sqlalchemy.orm import Session

from cruds.reservation import ReservationCRUD
from schemas.reservation import ReservationFilter, ReservationPaginationResponse, ReservationResponse, ReservationUpdate, ReservationCreate
from exceptions.http import NotFoundException, ConflictException
from models.reservation import ReservationModel


class ReservationService():
  def __init__(self, reservationCRUD: ReservationCRUD, db: Session):
    self._reservationCRUD: ReservationCRUD = reservationCRUD(db)

  async def get_all(
      self,
      filter: ReservationFilter,
      page: int = 1,
      size: int = 100,
  ):
    reservs: list[ReservationModel]
    totalItems: int
    reservs, totalItems = await self._reservationCRUD.get_all(
      filter=filter,
      offset=(page - 1) * size,
      limit=size,
    )
    
    reservItems: list[ReservationResponse] = []
    for reserv in reservs:
      reservItems.append(
        ReservationResponse(
          reservation_uid=reserv.reservation_uid,
          username=reserv.username,
          library_uid=reserv.library_uid,
          book_uid=reserv.book_uid,
          status=reserv.status,
          start_date=reserv.start_date,
          till_date=reserv.till_date,
        )
      )

    return ReservationPaginationResponse(
      page=page,
      pageSize=size,
      totalElements=totalItems,
      items=reservItems,
    )
  
  async def get_by_uid(
      self, 
      uid: UUID,
  ):
    reservation = await self._reservationCRUD.get_by_uid(uid)
    if reservation is None:
      raise NotFoundException(prefix="get reservation")
    
    return reservation

  async def create(
      self,
      reservation_create: ReservationCreate,
  ):
    reservation = ReservationModel(**reservation_create.model_dump())
    reservation = await self._reservationCRUD.create(reservation)
    if reservation is None:
      raise ConflictException(prefix="create reservation")
    
    return reservation
  
  async def patch(
      self,
      uid: UUID,
      reservation_patch: ReservationUpdate,
  ):
    reservation = await self._reservationCRUD.get_by_uid(uid)
    if reservation is None:
      raise NotFoundException(prefix="patch reservation")
    
    reservation = await self._reservationCRUD.update(reservation, reservation_patch)
    if reservation is None:
      raise ConflictException(prefix="patch reservation")
    
    return reservation
  
  async def delete(
      self,
      uid: UUID,
  ):
    reservation = await self._reservationCRUD.get_by_uid(uid)
    if reservation is None:
      raise NotFoundException(prefix="delete reservation")
    
    return await self._reservationCRUD.delete(reservation)
