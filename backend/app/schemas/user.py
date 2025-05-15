from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from app.schemas.dinner_option import DinnerOptionOut
from app.schemas.plus_one import PlusOneCreate, PlusOneOut

class UserBase(BaseModel):
  email: EmailStr
  full_name: str
  
class UserCreate(UserBase):
  password: str
  hashed_password: str | None = None
  plus_ones: list[PlusOneCreate] | None = None

class UserOut(UserBase):
  id: int
  is_active: bool
  is_admin: bool
  rsvp_confirmed: bool | None
  dietary_restrictions: str | None
  appetizer_option: DinnerOptionOut | None
  main_option: DinnerOptionOut | None
  plus_ones: list[PlusOneOut] | None = None
  created_at: datetime
  
  model_config = ConfigDict(from_attributes=True)
  
class UserUpdate(BaseModel):
    full_name:           str | None = None
    appetizer_option_id: int  | None = None
    main_option_id:      int  | None = None
    rsvp_confirmed:      bool | None = None
    dietary_restrictions:str | None = None