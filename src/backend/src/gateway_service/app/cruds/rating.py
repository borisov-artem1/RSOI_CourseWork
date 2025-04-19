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
from schemas.rating import Rating, RatingUpdate, RatingCreate


class RatingCRUD(BaseCRUD):
  def __init__(self):
    host = settings.options.gateway_service.rating_host
    port = settings.options.rating_service.port
    self.http_path = f'http://{host}:{port}/api/v1/'

  async def get_all_ratings(
    self,
    page: int = 1,
    size: int = 100,
    username: str | None = None,
    token: HTTPAuthorizationCredentials | None = None,
  ):
    validate_token_exists(token)
    
    response: Response = CircuitBreaker.send_request(
      url=f'{self.http_path}rating/?page={page}&size={size}'\
        f'{f"&username={username}" if username else ""}',
      http_method=requests.get,
      headers={
        AUTHORIZATION: token.scheme+SPACE+token.credentials,
      },
    )
    self._check_status_code(
      status_code=response.status_code,
      service_name="Rating Service",
    )

    rating_json: list[Rating] = response.json()

    ratings: list[Rating] = []
    for rating in rating_json:
      ratings.append(
        Rating(
          id=rating["id"],
          username=rating["username"],
          stars=rating["stars"],
        )
      )
    
    return ratings
  

  async def get_rating_by_id(
    self,
    id: int,
    token: HTTPAuthorizationCredentials | None = None,
  ) -> Rating:
    validate_token_exists(token)
    
    response: Response = CircuitBreaker.send_request(
      url=f'{self.http_path}rating/{id}',
      http_method=requests.get,
      headers={
        AUTHORIZATION: token.scheme+SPACE+token.credentials,
      },
    )
    self._check_status_code(
      status_code=response.status_code,
      service_name="Rating Service",
    )

    rating_json = response.json()

    return Rating(
      id=rating_json["id"],
      username=rating_json["username"],
      stars=rating_json["stars"],
    )
  

  async def add_rating(
    self,
    create: RatingCreate,
    token: HTTPAuthorizationCredentials | None = None,
  ) -> int:
    validate_token_exists(token)
    
    try:
      response: Response = requests.post(
        url=f'{self.http_path}rating/',
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
      service_name="Rating Service",
    )

    location: str = response.headers["location"]
    id = str(location.split("/")[-1])

    return id
  

  async def patch_rating(
    self,
    id: int,
    update: RatingUpdate,
    token: HTTPAuthorizationCredentials | None = None,
  ):
    validate_token_exists(token)
    
    try:
      response: Response = requests.patch(
        url=f'{self.http_path}rating/{id}',
        data=json.dumps(update.model_dump(exclude_unset=True)),
        headers={
          AUTHORIZATION: token.scheme+SPACE+token.credentials,
        },
      )
    except:
      response = Response()
      response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    self._check_status_code(
      status_code=response.status_code,
      service_name="Rating Service",
    )

    rating = response.json()
    return rating["id"]
