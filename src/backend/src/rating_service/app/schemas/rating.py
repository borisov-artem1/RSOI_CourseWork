from typing import Annotated
from fastapi import Query
from pydantic import BaseModel, constr, conint


class RatingBase(BaseModel):
  username: Annotated[str, constr(max_length=80)]
  stars: Annotated[int, conint(ge=1, le=100)]


class RatingFilter(BaseModel):
  username: Annotated[str, Query(max_length=800)] | None = None
  stars: Annotated[int, Query(ge=1,le=100)] | None = None
  

class RatingUpdate(BaseModel):
  username: Annotated[str, constr(max_length=80)] | None = None
  stars: Annotated[int, conint(ge=1, le=100)] | None = None


class RatingCreate(RatingBase):
  pass


class Rating(RatingBase):
  id: int
