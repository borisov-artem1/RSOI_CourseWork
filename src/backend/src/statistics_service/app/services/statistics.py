from sqlalchemy.orm import Session

from schemas.statistics import StatisticsResponse, StatisticsPaginationResponse
from models.statistics import StatisticsModel
from cruds.statistics import StatisticsCRUD


class StatisticsService():
  def __init__(self, statisticsCRUD: StatisticsCRUD, db: Session):
    self._statisticsCRUD: StatisticsCRUD = statisticsCRUD(db)
    
  async def get_all(
    self,
    page: int = 1,
    size: int = 100,
  ):
    statistics: list[StatisticsModel]
    totalItems: int
    statistics, totalItems = await self._statisticsCRUD.get_all(
      offset=(page - 1) * size,
      limit=size,
    )
    
    statisticsItems: list[StatisticsResponse] = []
    for statistic in statistics:
      statisticsItems.append(
        StatisticsResponse(
          id=statistic.id,
          method=statistic.method,
          url=statistic.url,
          status_code=statistic.status_code,
          time=statistic.time,
        )
      )

    return StatisticsPaginationResponse(
      page=page,
      pageSize=size,
      totalElements=totalItems,
      items=statisticsItems,
    )
  