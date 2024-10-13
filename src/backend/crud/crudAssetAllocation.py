# app/crud.py
from sqlalchemy.orm import Session
from models import PortfolioAssetAllocation
from datetime import datetime
from datetime import date

def allocate_asset_to_portfolio(db: Session, portfolio_id: int, asset_id: int, quantity: float, purchase_price: float):
    allocation = PortfolioAssetAllocation(
        PortfolioID=portfolio_id,
        AssetID=asset_id,
        quantity=quantity,
        purchase_price=purchase_price
    )
    db.add(allocation)
    db.commit()
    db.refresh(allocation)
    return allocation


# app/crud.py
def deallocate_asset_from_portfolio(db: Session, allocation_id: int):
    allocation = db.query(PortfolioAssetAllocation).filter(PortfolioAssetAllocation.AllocationID == allocation_id).first()
    
    if allocation and allocation.is_allocated:
        allocation.valid_to = datetime.utcnow()
        allocation.is_allocated = False
        db.commit()
        db.refresh(allocation)
    return allocation



def get_allocations(db: Session, startDate: date, endDate: date, skip: int = 0, limit: int = 10):
    return db.query(PortfolioAssetAllocation).filter(PortfolioAssetAllocation.allocated_at >= startDate, PortfolioAssetAllocation.allocated_at <= endDate).offset(skip).limit(limit).all()


def get_allocations_portfolio(db: Session, portfolio_id: int, startDate: date, endDate: date, skip: int = 0, limit: int = 10):
    return db.query(PortfolioAssetAllocation).filter(PortfolioAssetAllocation.PortfolioID == portfolio_id, PortfolioAssetAllocation.allocated_at >= startDate, PortfolioAssetAllocation.allocated_at <= endDate).offset(skip).limit(limit).all()



