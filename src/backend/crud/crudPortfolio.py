# crud.py
from sqlalchemy.orm import Session
from models import Portfolio, Portfolio, Asset, Trade, MarketData, RiskMetric
from schemas import PortfolioCreate, PortfolioCreate, AssetCreate, TradeCreate, MarketDataCreate, RiskMetricCreate

from datetime import datetime

def create_portfolio(db: Session, portfolio: PortfolioCreate):
    db_portfolio = Portfolio(**portfolio.dict())
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

def get_portfolios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Portfolio).offset(skip).limit(limit).all()


def get_portfolio(db: Session, portfolio_id: int):
    return db.query(Portfolio).filter(Portfolio.PortfolioID == portfolio_id).first()

# Update an Portfolio by ID
def update_portfolio(db: Session, portfolio_id: int, Portfolio: PortfolioCreate):
    db_Portfolio = get_portfolio(db, portfolio_id)
    if db_Portfolio:
        for key, value in Portfolio.dict().items():
            setattr(db_Portfolio, key, value)
        
        db.commit()
        db.refresh(db_Portfolio)
    return db_Portfolio



def deactivate_portfolio(db: Session, portfolio_id: int):
    db_Portfolio = get_portfolio(db, portfolio_id)
    if db_Portfolio:
        db_Portfolio.is_active = False  # Set is_active to False
        db_Portfolio.inactive_at = datetime.utcnow()  # Set the current timestamp for inactive_at
        db.commit()
        db.refresh(db_Portfolio)  # Refresh to get the updated data
    return db_Portfolio