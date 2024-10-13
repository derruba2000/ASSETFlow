# app/api/endpoints/assets.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from schemas import MarketData, MarketDataCreate
from crud.crudMarketData import create_market_data, get_market_data, get_market_data_asset
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
@router.post("/", response_model=MarketData)
def create_new_asset(market_data: MarketDataCreate, db: Session = Depends(get_db)):
    db_market_data = create_market_data(db=db, market_data=market_data)
    return db_market_data

# GET: Retrieve market data for a date range
@router.get("/readAll", response_model=List[MarketData])
def read_market_data_all(
    StartDate: date,
    EndDate: date,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    market_data = get_market_data(db=db, startDate=StartDate, endDate=EndDate , skip=skip, limit=limit)
    if not market_data:
        raise HTTPException(status_code=404, detail="No market data found for the given date range")
    return market_data


# GET: Retrieve market data for a specific asset within a date range
@router.get("/{assetId}", response_model=List[MarketData])
def read_market_data(
    assetId: int,
    StartDate: date,
    EndDate: date,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    market_data = get_market_data_asset(db=db, asset_id=assetId, startDate=StartDate, endDate=EndDate, skip=skip, limit=limit)
    if market_data is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    if not market_data:
        raise HTTPException(status_code=404, detail="No market data found for the given date range")
    return market_data




