from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SAEnum
from app.db.base import Base

class DinnerCategory(str, Enum):
  appetizer = "appetizer"
  entree    = "entree"
  
class DinnerOption(Base):
  __tablename__ = "dinner_options"
  
  id        = Column(Integer, primary_key=True, index=True)
  name      = Column(String, nullable=False)
  category  = Column(SAEnum(DinnerCategory), nullable=False, index=True)