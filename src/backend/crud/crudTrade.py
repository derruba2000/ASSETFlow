# crud.py
from sqlalchemy.orm import Session
from models import Trade
from schemas import  TradeCreate

from datetime import date

def create_trade(db: Session, trade: TradeCreate):
    db_trade = Trade(**trade.dict())
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade

def get_trades(db: Session, startDate: date, endDate: date, skip: int = 0, limit: int = 10):
    return db.query(Trade).filter(Trade.TradeDate >= startDate, Trade.TradeDate <= endDate).offset(skip).limit(limit).all()


def get_trades_asset(db: Session, asset_id: int, startDate: date, endDate: date, skip: int = 0, limit: int = 10):
    return db.query(Trade).filter(Trade.AssetID == asset_id, Trade.TradeDate >= startDate, Trade.TradeDate <= endDate).offset(skip).limit(limit).all()


def get_trades_portfolio(db: Session, portfolio_id: int, startDate: date, endDate: date, skip: int = 0, limit: int = 10):
    return db.query(Trade).filter(Trade.PortfolioID == portfolio_id, Trade.TradeDate >= startDate, Trade.TradeDate <= endDate).offset(skip).limit(limit).all()




