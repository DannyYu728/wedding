from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.dinner_option import DinnerOptionOut
from app.schemas.plus_one import PlusOneCreate, PlusOneOut

class UserBase(BaseModel):
  email: EmailStr
  full_name: str
  
class UserCreate(UserBase):
  password: str
  plus_ones: list[PlusOneCreate] | None = None

class UserOut(UserBase):
  id: int
  is_active: bool
  is_admin: bool
  rsvp_confirmed: bool
  dietary_restrictions: str | None
  appetizer_option: DinnerOptionOut | None
  main_option: DinnerOptionOut | None
  plus_ones: list[PlusOneOut] | None = None
  created_at: datetime
  
class UserUpdate(BaseModel):
  appetizer_option_id: int | None
  main_option_id: int | None
  rsvp_confirmed: bool | None
  dietary_restrictions: str | None