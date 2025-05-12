from pydantic import BaseModel
from app.schemas.dinner_option import DinnerOptionOut

class PlusOneCreate(BaseModel):
    full_name:           str
    appetizer_option_id: int | None
    main_option_id:      int | None
    dietary_restrictions: str | None

class PlusOneUpdate(BaseModel):
    full_name:            str | None
    appetizer_option_id:  int | None
    main_option_id:       int | None
    dietary_restrictions: str | None

class PlusOneOut(BaseModel):
    id:                   int
    full_name:            str
    appetizer_option:     DinnerOptionOut | None
    main_option:          DinnerOptionOut | None
    dietary_restrictions: str | None

    class Config:
        orm_mode = True
