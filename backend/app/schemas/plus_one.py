from pydantic import BaseModel
from typing import Optional
from app.schemas.dinner_option import DinnerOptionOut

class PlusOneCreate(BaseModel):
    full_name:           str
    appetizer_option_id: Optional[int]
    main_option_id:      Optional[int]
    dietary_restrictions: Optional[str]

class PlusOneUpdate(BaseModel):
    full_name:            Optional[str]
    appetizer_option_id:  Optional[int]
    main_option_id:       Optional[int]
    dietary_restrictions: Optional[str]

class PlusOneOut(BaseModel):
    id:                   int
    full_name:            str
    appetizer_option:     Optional[DinnerOptionOut]
    main_option:          Optional[DinnerOptionOut]
    dietary_restrictions: Optional[str]

    class Config:
        orm_mode = True
