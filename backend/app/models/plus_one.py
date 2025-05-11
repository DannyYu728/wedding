from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Plus_One(Base):
    __tablename__ = "plus_ones"

    id                   = Column(Integer, primary_key=True, index=True)
    user_id              = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    full_name            = Column(String, nullable=False)
    dietary_restrictions = Column(String, nullable=True)

    appetizer_option_id = Column(Integer, ForeignKey("dinner_options.id"), nullable=True)
    main_option_id = Column(Integer, ForeignKey("dinner_options.id"), nullable=True)

    appetizer_option = relationship("DinnerOption", foreign_keys=[appetizer_option_id], lazy="joined")
    main_option = relationship("DinnerOption", foreign_keys=[main_option_id], lazy="joined")   
    
    user = relationship("User", back_populates="plus_one")