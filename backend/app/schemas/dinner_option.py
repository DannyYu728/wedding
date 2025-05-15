from enum import Enum
from pydantic import BaseModel, ConfigDict

class DinnerCategory(str, Enum):
  appetizer = "appetizer"
  entree = "entree" 
  
class DinnerOptionOut(BaseModel):
  id: int
  name: str
  category: DinnerCategory
  
  model_config = ConfigDict(from_attributes=True)