from uuid import UUID
from fastapi import Response, status

from enums.enums import DomainEnum

class CreatedResponse(Response):
  def __init__(self, domain: DomainEnum, id: int | UUID):
    super().__init__(
      status_code=status.HTTP_201_CREATED,
      headers={"Location": f"/api/v1/{domain.lower()}/{id}"},  
    )

class NoContentResponse(Response):
  def __init__(self):
    super().__init__(
      status_code=status.HTTP_204_NO_CONTENT,
    )
    
class OkResponse(Response):
  def __init__(self):
    super().__init__(
      status_code=status.HTTP_200_OK,
    )
