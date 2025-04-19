from typing import Annotated
from pydantic import BaseModel, constr, conint


class RatingBase(BaseModel):
  username: Annotated[str, constr(max_length=80)]
  stars: Annotated[int, conint(ge=1, le=100)]


class RatingUpdate(BaseModel):
  username: Annotated[str, constr(max_length=80)] | None = None
  stars: Annotated[int, conint(ge=1, le=100)] | None = None


class RatingCreate(RatingBase):
  pass


class Rating(RatingBase):
  id: int


class UserRatingResponse(BaseModel):
  stars: Annotated[int, conint(ge=1, le=100)]
