from pydantic import BaseModel, ConfigDict

from enums.enums import DomainEnum

class BaseApiResponses:
  def __init__(self, domain_name: DomainEnum):
    self.domain_name = domain_name
    
  def not_authorized(self):
    return {
      "model": NotAuthorizedResponse,
      "description": f"User in domain {self.domain_name} is not authorized",
    }
    
  def forbidden(self):
    return {
      "model": ForbiddenResponse,
      "description": f"Method in domain {self.domain_name} forbidden to access",
    }
    
  def invalid_data(self):
    return {
      "model": ValidationErrorResponse,
      "description": f"Invalid data for {self.domain_name} entity",
    }
    
  def not_found(self):
    return {
      "model": ErrorResponse,
      "description": f"Not found {self.domain_name} by uuid",
    }
    
  def conflict(self):
    return {
      "model": ErrorResponse,
      "description": f"Conflict for {self.domain_name} entity",
    }
    
  def health(self):
    return {
      "description": f"{self.domain_name} server is ready to work",
      "content": {
        "application/octet-stream": {
          "example": ""
        }
      },
    }
    
    
    
class GatewayApiResponses(BaseApiResponses):
  def __init__(self):
    super(GatewayApiResponses, self).__init__(domain_name = DomainEnum.GATEWAY)
    self.domain_name = DomainEnum.GATEWAY
    
  def get_all_libraries_in_city(self):
    return {
      "description": "Все библиотеки в городе",
    }
    
  def get_all_books_in_library(self):
    return {
      "description": "Все кники в библиотеке по uuid",
    }
    
  def get_user_rented_books(self):
    return {
      "description": "Все взятые пользователем книги",
    }
    
  def get_user_rating(self):
    return {
      "description": "Рейтинг пользователя",
    }
    
  def take_book(self):
    return {
      "description": "Взять книгу",
    }
    
  def return_book(self):
    return {
      "description": "Вернуть книгу",
    }
    
  def reservation_not_found(self):
    return {
      "model": ErrorResponse,
      "description": "Бронирование не найдено",
    }
    
  
    
class ForbiddenResponse(BaseModel):
  model_config = ConfigDict(
    json_schema_extra = {
      "example": {
        "message": "Error: Forbidden"
      },
    }
  )
    
class NotAuthorizedResponse(BaseModel):
  model_config = ConfigDict(
    json_schema_extra = {
      "example": {
        "message": "Error: Not Authorized"
      },
    }
  )

class ErrorResponse(BaseModel):
  model_config = ConfigDict(
    json_schema_extra = {
      "example": {
        "message": "Method: exception description"
      },
    }
  )

class ValidationErrorResponse(BaseModel):
  model_config = ConfigDict(
    json_schema_extra = {
      "example": {
        "message": "Invalid request",
        "errors": [
          {
            "type": "type of error",
            "msg": "error message",
            "loc": "error location"
          }
        ]
      }
    }
  )
