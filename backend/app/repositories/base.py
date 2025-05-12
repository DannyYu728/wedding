from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class AbstractRepo (ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
  @abstractmethod
  async def get(self, id: int) -> Optional[ModelType]:
    pass
  
  @abstractmethod
  async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
    pass
  
  @abstractmethod
  async def create(self, obj_in: CreateSchemaType) -> ModelType:
    pass
  
  @abstractmethod
  async def update(self, id: int, obj_in: UpdateSchemaType) -> ModelType:
    pass
  
  @abstractmethod
  async def delete(self, id: int) -> None:
    pass