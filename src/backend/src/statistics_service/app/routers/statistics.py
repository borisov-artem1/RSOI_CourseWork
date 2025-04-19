from fastapi import APIRouter, Body, Depends, Query, status
from typing import Annotated
from confluent_kafka import Producer
from sqlalchemy.orm import Session
from schemas.statistics import StatisticsPaginationResponse, StatisticsCreate
from utils.database import get_db
import json

from schemas.api_response import ApiResponses
from enums.enums import DomainEnum, RoleEnum
from services.statistics import StatisticsService
from cruds.statistics import StatisticsCRUD
from utils.auth_user import RoleChecker


def get_statistics_crud() -> StatisticsCRUD:
  return StatisticsCRUD

def get_statistics_service(
  statistics_crud: Annotated[StatisticsCRUD, Depends(get_statistics_crud)],
  db: Annotated[Session, Depends(get_db)],
) -> StatisticsService:
  return StatisticsService(
    statisticsCRUD=statistics_crud,
    db=db,
  )

router = APIRouter(
  prefix="/statistics",
  tags=["Statistics API"],
  responses={
    status.HTTP_400_BAD_REQUEST: ApiResponses.invalid_data(DomainEnum.STATISTICS),
  }
)

producer_conf = {
  'bootstrap.servers': 'kafka:29092',
  'client.id': 'my-app',
}

producer = Producer(producer_conf)

@router.post(
  path="/produce",
  status_code=status.HTTP_201_CREATED,
  response_model={},
)
async def produce(
  statistics_produce: Annotated[StatisticsCreate, Body()],
):
  producer.produce('my-topic', value=statistics_produce.model_dump_json().encode('utf-8'))
  producer.flush()
  return {"status": "success"}

@router.get(
  path="/",
  status_code=status.HTTP_200_OK,
  response_model=StatisticsPaginationResponse,
  responses={
    status.HTTP_200_OK: ApiResponses.get_all(DomainEnum.STATISTICS),
    status.HTTP_401_UNAUTHORIZED: ApiResponses.not_authorized(DomainEnum.STATISTICS),
    status.HTTP_403_FORBIDDEN: ApiResponses.forbidden(DomainEnum.STATISTICS),
  },
)
async def get_all(
  statistics_service: Annotated[StatisticsService, Depends(get_statistics_service)],
  page: Annotated[int, Query(ge=1)] = 1,
  size: Annotated[int, Query(ge=1)] = 100,
  _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.ADMIN])),
):
  return await statistics_service.get_all(
    page=page,
    size=size,
  )
