from sqlalchemy.orm import Session

from models.statistics import StatisticsModel


class StatisticsCRUD():
  def __init__(self, db: Session):
    self._db = db
    
  async def get_all(
    self,
    offset: int = 0,
    limit: int = 100,
  ) -> list[list[StatisticsModel], int]:
    statistics = self._db.query(StatisticsModel)
    total = statistics.count()
    statistics = statistics.order_by(StatisticsModel.id.desc())
    
    return statistics.offset(offset).limit(limit).all(), total
