# crud.py
from sqlalchemy.orm import Session
from models import MarketData
from schemas import  MarketDataCreate

from datetime import date

def create_market_data(db: Session, market_data: MarketDataCreate):
    db_market_data = MarketData(**market_data.dict())
    db.add(db_market_data)
    db.commit()
    db.refresh(db_market_data)
    return db_market_data

def get_market_data(db: Session, startDate: date, endDate: date, skip: int = 0, limit: int = 10):
    return db.query(MarketData).filter(MarketData.Date >= startDate, MarketData.Date <= endDate).offset(skip).limit(limit).all()


def get_market_data_asset(db: Session, asset_id: int, startDate: date, endDate: date, skip: int = 0, limit: int = 10):
    return db.query(MarketData).filter(MarketData.AssetID == asset_id, MarketData.Date >= startDate, MarketData.Date <= endDate).offset(skip).limit(limit).all()




