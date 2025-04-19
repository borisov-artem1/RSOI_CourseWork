import json
from uuid import UUID
from fastapi.security import HTTPAuthorizationCredentials
import requests
from requests import Response
from fastapi import status

from utils.consts import AUTHORIZATION, SPACE
from utils.validate import validate_token_exists
from cruds.base import BaseCRUD
from utils.settings import settings
from utils.circuit_breaker import CircuitBreaker
from schemas.reservation import Reservation, ReservationCreate, ReservationPaginationResponse, ReservationUpdate
from enums.status import ReservationStatus


class ReservationCRUD(BaseCRUD):
  def __init__(self):
    host = settings.options.gateway_service.reservation_host
    port = settings.options.reservation_service.port
    self.http_path = f'http://{host}:{port}/api/v1/'

  async def get_all_reservations(
    self,
    page: int = 1,
    size: int = 100,
    username: str | None = None,
    status: ReservationStatus | None = None,
    token: HTTPAuthorizationCredentials | None = None,
  ):
    validate_token_exists(token)
    
    response: Response = CircuitBreaker.send_request(
      url=f'{self.http_path}reservation/?page={page}&size={size}'\
        f'{f"&username={username}" if username else ""}'\
        f'{f"&status={status}" if status else ""}',
      http_method=requests.get,
      headers={
        AUTHORIZATION: token.scheme+SPACE+token.credentials,
      },
    )
    self._check_status_code(
      status_code=response.status_code,
      service_name="Reservation Service",
    )

    reservation_json = response.json()
    reservations = reservation_json["items"]

    reservations_items: list[Reservation] = []
    for reservation in reservations:
      reservations_items.append(
        Reservation(
          reservationUid=reservation["reservation_uid"],
          username=reservation["username"],
          bookUid=reservation["book_uid"],
          libraryUid=reservation["library_uid"],
          status=reservation["status"],
          startDate=reservation["start_date"],
          tillDate=reservation["till_date"],
        )
      )
    
    return ReservationPaginationResponse(
      page=page,
      pageSize=size,
      totalElements=reservation_json["totalElements"],
      items=reservations_items,
    )
    

  async def get_reservation_by_uid(
    self,
    uid: UUID,
    token: HTTPAuthorizationCredentials | None = None,
  ) -> Reservation:
    validate_token_exists(token)
    
    response: Response = CircuitBreaker.send_request(
      url=f'{self.http_path}reservation/{uid}',
      http_method=requests.get,
      headers={
        AUTHORIZATION: token.scheme+SPACE+token.credentials,
      },
    )
    self._check_status_code(
      status_code=response.status_code,
      service_name="Reservation Service",
    )
    
    reservation = response.json()
    
    return Reservation(
      reservationUid=reservation["reservation_uid"],
      username=reservation["username"],
      bookUid=reservation["book_uid"],
      libraryUid=reservation["library_uid"],
      status=reservation["status"],
      startDate=reservation["start_date"],
      tillDate=reservation["till_date"],
    )
  

  async def patch_reservation(
    self,
    uid: UUID,
    update: ReservationUpdate,
    token: HTTPAuthorizationCredentials | None = None,
  ):
    validate_token_exists(token)
    
    update.book_uid = None if not update.book_uid else str(update.book_uid) # is not JSON serializable
    update.library_uid = None if not update.library_uid else str(update.library_uid) # is not JSON serializable
    update.start_date = None if not update.start_date else update.start_date.strftime('%Y-%m-%d') # is not JSON serializable
    update.till_date = None if not update.till_date  else update.till_date.strftime('%Y-%m-%d') # is not JSON serializable

    try:
      response: Response = requests.patch(
        url=f'{self.http_path}reservation/{uid}',
        data=json.dumps(update.model_dump(mode='json', exclude_unset=True, exclude_none=True)),
        headers={
          AUTHORIZATION: token.scheme+SPACE+token.credentials,
        },
      )
    except:
      response = Response()
      response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    self._check_status_code(
      status_code=response.status_code,
      service_name="Reservation Service",
    )

    reservation = response.json()
    return reservation["id"]
  

  async def add_reservation(
    self,
    create: ReservationCreate,
    token: HTTPAuthorizationCredentials | None = None,
  ) -> UUID:
    validate_token_exists(token)
    
    create.book_uid = str(create.book_uid) # is not JSON serializable
    create.library_uid = str(create.library_uid) # is not JSON serializable
    create.start_date = create.start_date.strftime('%Y-%m-%d') # is not JSON serializable
    create.till_date = create.till_date.strftime('%Y-%m-%d') # is not JSON serializable

    try:
      response: Response = requests.post(
        url=f'{self.http_path}reservation/',
        data=json.dumps(create.model_dump()),
        headers={
          AUTHORIZATION: token.scheme+SPACE+token.credentials,
        },
      )
    except:
      response = Response()
      response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    self._check_status_code(
      status_code=response.status_code,
      service_name="Reservation Service",
    )

    location: str = response.headers["location"]
    uid = str(location.split("/")[-1])

    return uid
  

  async def delete_reservation(
    self,
    uid: UUID,
    token: HTTPAuthorizationCredentials | None = None,  
  ):
    validate_token_exists(token)
    
    try:
      response: Response = requests.delete(
        url=f'{self.http_path}reservations/{uid}/',
        headers={
          AUTHORIZATION: token.scheme+SPACE+token.credentials,
        },
      )
    except:
      response = Response()
      response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
  
    self._check_status_code(
      status_code=response.status_code,
      service_name="Reservation Service"
    )
