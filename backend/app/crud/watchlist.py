from sqlalchemy.orm import Session
from app.models.watchlist import WatchlistAsset
from app.schemas.watchlist import WatchlistAssetCreate, WatchlistAssetUpdate

def get_assets_by_owner(db: Session, owner_id: int):
    return db.query(WatchlistAsset).filter(WatchlistAsset.owner_id == owner_id).all()

def get_all_assets(db: Session):
    return db.query(WatchlistAsset).all()

def get_asset_by_id(db: Session, asset_id: int):
    return db.query(WatchlistAsset).filter(WatchlistAsset.id == asset_id).first()

def create_asset(db: Session, asset_in: WatchlistAssetCreate, owner_id: int):
    asset = WatchlistAsset(**asset_in.model_dump(), owner_id=owner_id)
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset

def update_asset(db: Session, asset: WatchlistAsset, updates: WatchlistAssetUpdate):
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(asset, field, value)
    db.commit()
    db.refresh(asset)
    return asset

def delete_asset(db: Session, asset: WatchlistAsset):
    db.delete(asset)
    db.commit()
