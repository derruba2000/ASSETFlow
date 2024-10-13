# app/api/endpoints/assets.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas import Asset, AssetCreate
from crud.crudAsset import create_asset, get_assets, get_asset, update_asset
from database import SessionLocal

router = APIRouter()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST: Create a new asset
@router.post("/", response_model=Asset)
def create_new_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    db_asset = create_asset(db=db, asset=asset)
    return db_asset

# GET: Retrieve all assets
@router.get("/", response_model=List[Asset])
def read_assets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    assets = get_assets(db=db, skip=skip, limit=limit)
    return assets


# GET: Retrieve a specific asset by ID
@router.get("/{asset_id}", response_model=Asset)
def read_asset(asset_id: int, db: Session = Depends(get_db)):
    db_asset = get_asset(db=db, asset_id=asset_id)
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db_asset

# PUT: Update an existing Asset by TickerSymbol
@router.put("/{TickerSymbol}", response_model=Asset)
def update_existing_asset(tickersymbol: str, asset: AssetCreate, db: Session = Depends(get_db)):
    db_asset = update_asset(db=db, tickersymbol=tickersymbol, asset=asset)
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db_asset

