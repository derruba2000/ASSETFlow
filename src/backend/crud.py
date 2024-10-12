# crud.py
from sqlalchemy.orm import Session
from models.models import Investor, Portfolio, Asset, Trade, MarketData, RiskMetric
from schemas.schemas import InvestorCreate, PortfolioCreate, AssetCreate, TradeCreate, MarketDataCreate, RiskMetricCreate

def create_investor(db: Session, investor: InvestorCreate):
    db_investor = Investor(**investor.dict())
    db.add(db_investor)
    db.commit()
    db.refresh(db_investor)
    return db_investor

def get_investors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Investor).offset(skip).limit(limit).all()


def get_investor(db: Session, investor_id: int):
    return db.query(Investor).filter(Investor.InvestorID == investor_id).first()

# Update an investor by ID
def update_investor(db: Session, investor_id: int, investor: InvestorCreate):
    db_investor = get_investor(db, investor_id)
    if db_investor:
        for key, value in investor.dict().items():
            setattr(db_investor, key, value)
        
        db.commit()
        db.refresh(db_investor)
    return db_investor