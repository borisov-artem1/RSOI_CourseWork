from sqlalchemy.orm import Session
from abc import ABC, abstractmethod

from models.statistics import StatisticsModel


class IStatisticsCRUD(ABC):
    def __init__(self, db: Session):
        self._db = db

    @abstractmethod
    async def get_all(self) -> list[StatisticsModel]:
       pass
