# app/api/endpoints/assets.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas import Asset, AssetCreate, MultipleAssetsCreate
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


# Read total number of Assets
@router.get("/assetcount", response_model=int)
def read_total_assets(db: Session = Depends(get_db)):
    iterationSize=40
    totalAssets=0
    while True:
        assets = get_assets(db=db, skip=totalAssets, limit=iterationSize)
        if len(assets) < iterationSize:
            break 
        totalAssets += len(assets)
    return totalAssets

# GET: Retrieve an asset by ticker symbol
@router.get("/asset/{tickersymbol}", response_model=Asset)
def read_asset_by_ticker(tickersymbol: str, db: Session = Depends(get_db)):
    db_asset = get_asset(db=db, tickersymbol=tickersymbol)
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db_asset

# GET: Retrieve a specific asset by ID
@router.get("/{asset_id}", response_model=Asset)
def read_asset(asset_id: int, db: Session = Depends(get_db)):
    db_asset = get_asset(db=db, asset_id=asset_id)
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db_asset

# PUT: Update an existing Asset by TickerSymbol
@router.put("/{tickersymbol}", response_model=Asset)
def update_existing_asset(tickersymbol: str, asset: AssetCreate, db: Session = Depends(get_db)):
    db_asset = update_asset(db=db, tickersymbol=tickersymbol, Asset=asset)
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db_asset

# Create multiple assets
@router.post("/bulk", response_model=List[AssetCreate])
def create_multiple_assets(asset_data: MultipleAssetsCreate, db: Session = Depends(get_db)):
    created_assets = []
    for asset in asset_data.assets:
        db_asset = create_asset(db=db, asset=asset)
        created_assets.append(db_asset)
    return created_assets


