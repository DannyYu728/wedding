from enum import Enum
from pydantic import BaseModel

class DinnerCategory(str, Enum):
  appetizer = "appetizer"
  entree = "entree" 
  
class DinnerOptionOut(BaseModel):
  id: int
  name: str
  category: DinnerCategory
  
  class Config:
    orm_mode = True