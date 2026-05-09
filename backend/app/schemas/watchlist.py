from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WatchlistAssetCreate(BaseModel):
    symbol: str
    asset_name: str
    target_price: float
    current_price: Optional[float] = None
    notes: Optional[str] = None

class WatchlistAssetUpdate(BaseModel):
    symbol: Optional[str] = None
    asset_name: Optional[str] = None
    target_price: Optional[float] = None
    current_price: Optional[float] = None
    notes: Optional[str] = None

class WatchlistAssetResponse(BaseModel):
    id: int
    symbol: str
    asset_name: str
    target_price: float
    current_price: Optional[float]
    notes: Optional[str]
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
