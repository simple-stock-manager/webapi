from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InventoryItemBase(BaseModel):
    name: str
    category: Optional[str] = None
    quantity: Optional[int] = 0
    unit: Optional[str] = None


class CreateInventoryItem(InventoryItemBase):
    pass


class UpdateInventoryItem(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None


class InventoryItemResponse(InventoryItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
