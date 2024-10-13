# app/api/endpoints/assets.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas import Trade, TradeCreate
from crud.crudTrade import create_trade, get_trades, get_trades_asset, get_trades_portfolio
from database import SessionLocal
from datetime import date

router = APIRouter()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST: Create a new trade
@router.post("/", response_model=Trade)
def create_new_trade(trade: TradeCreate, db: Session = Depends(get_db)):
    db_asset = create_trade(db=db, trade=trade)
    return db_asset

# GET: Retrieve all trades
@router.get("/getAll", response_model=List[Trade])
def read_trades( StartDate: date, EndDate : date ,skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    trades = get_trades(db=db, skip=skip, limit=limit, startDate=StartDate, endDate=EndDate)
    return trades


# GET: Retrieve all the trades by assetid
@router.get("/getAsset", response_model=List[Trade])
def read_asset_by_ticker(StartDate : date, EndDate : date, asset_id: int, skip: int = 0, limit: int = 10,  db: Session = Depends(get_db)):
    trades = get_trades_asset(db=db, asset_id=asset_id, startDate=StartDate, endDate=EndDate, skip=skip, limit=limit)
    if trades is None:
        raise HTTPException(status_code=404, detail="Not trades for this asset")
    return trades

# GET: Retrieve all the trades by portfolioid
@router.get("/getPortfolio", response_model=List[Trade])
def read_asset_by_ticker(StartDate : date, EndDate : date, portfolio_id: int, skip: int = 0, limit: int = 10,  db: Session = Depends(get_db)):
    trades = get_trades_portfolio(db=db, portfolio_id=portfolio_id, startDate=StartDate, endDate=EndDate, skip=skip, limit=limit)
    if trades is None:
        raise HTTPException(status_code=404, detail="Not trades for this asset")
    return trades



