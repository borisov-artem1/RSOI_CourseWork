from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from enums.enums import RoleEnum


class UserPayloadDto(BaseModel):
  sub: UUID
  login: str
  role: RoleEnum
  email: EmailStr | None = None
  phone: PhoneNumber | None = None
  lastname: str | None = None
  firstname: str | None = None
  type: str | None = None
  exp: datetime
  iat: datetime
