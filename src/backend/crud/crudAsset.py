# crud.py
from sqlalchemy.orm import Session
from models import Portfolio, Portfolio, Asset, Trade, MarketData, RiskMetric
from schemas import PortfolioCreate, PortfolioCreate, AssetCreate, TradeCreate, MarketDataCreate, RiskMetricCreate

from datetime import datetime

def create_asset(db: Session, asset: AssetCreate):
    db_asset = Asset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

def get_assets(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Asset).offset(skip).limit(limit).all()


def get_asset(db: Session, tickersymbol: str):
    return db.query(Asset).filter(Asset.TickerSymbol == tickersymbol).first()

# Update an Asset by Tyckersymbol
def update_asset(db: Session, tickersymbol: str, Asset: AssetCreate):
    db_asset = get_asset(db, tickersymbol)
    if db_asset:
        for key, value in Asset.dict().items():
            setattr(db_asset, key, value)
        
        db.commit()
        db.refresh(db_asset)
    return db_asset



