from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.watchlist import WatchlistAssetCreate, WatchlistAssetUpdate, WatchlistAssetResponse
from app.crud.watchlist import (
    get_assets_by_owner, get_all_assets,
    get_asset_by_id, create_asset, update_asset, delete_asset
)
from app.core.dependencies import get_current_user, get_admin_user
from app.models.user import User

router = APIRouter(prefix="/watchlist", tags=["Watchlist"])

@router.post("/", response_model=WatchlistAssetResponse, status_code=status.HTTP_201_CREATED)
def add_asset(asset_in: WatchlistAssetCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_asset(db, asset_in, owner_id=current_user.id)

@router.get("/", response_model=List[WatchlistAssetResponse])
def list_my_assets(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_assets_by_owner(db, current_user.id)

@router.get("/all", response_model=List[WatchlistAssetResponse])
def list_all_assets(db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    return get_all_assets(db)

@router.put("/{asset_id}", response_model=WatchlistAssetResponse)
def edit_asset(asset_id: int, updates: WatchlistAssetUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    asset = get_asset_by_id(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    if asset.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your asset")
    return update_asset(db, asset, updates)

@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_asset(asset_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    asset = get_asset_by_id(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    if asset.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    delete_asset(db, asset)
