from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.dinner_option import DinnerOptionOut
from app.schemas.plus_one import PlusOneCreate, PlusOneOut

class UserBase(BaseModel):
  email: EmailStr
  full_name: str
  
class UserCreate(UserBase):
  password: str
  plus_ones: Optional[list[PlusOneCreate]] = None

class UserOut(UserBase):
  id: int
  is_active: bool
  is_admin: bool
  rsvp_confirmed: bool
  dietary_restrictions: Optional[str]
  appetizer_option: Optional[DinnerOptionOut]
  main_option: Optional[DinnerOptionOut]
  plus_ones: Optional[list[PlusOneOut]] = None
  created_at: datetime
  
class UserUpdate(BaseModel):
  appetizer_option_id: Optional[int]
  main_option_id: Optional[int]
  rsvp_confirmed: Optional[bool]
  dietary_restrictions: Optional[str]