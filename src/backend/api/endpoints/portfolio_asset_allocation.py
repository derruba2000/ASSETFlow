# app/api/endpoints/portfolio_asset_allocation.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import PortfolioAssetAllocationCreate, PortfolioAssetAllocation
from crud.crudAssetAllocation import allocate_asset_to_portfolio, deallocate_asset_from_portfolio, get_allocations, get_allocations_portfolio
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

# POST: Allocate an asset to a portfolio
@router.post("/portfolio/{portfolio_id}/allocate", response_model=PortfolioAssetAllocation)
def allocate_asset(
    portfolio_id: int,
    asset_id: int,
    quantity: float,
    purchase_price: float,
    db: Session = Depends(get_db)
):
    allocation = allocate_asset_to_portfolio(db=db, portfolio_id=portfolio_id, asset_id=asset_id, quantity=quantity, purchase_price=purchase_price)
    if not allocation:
        raise HTTPException(status_code=404, detail="Allocation failed")
    return allocation


# api/endpoints/portfolio_asset_allocation.py
# PUT: Deallocate an asset from a portfolio
@router.put("/deallocate/{allocation_id}", response_model=PortfolioAssetAllocation)
def deallocate_asset(allocation_id: int,  db: Session = Depends(get_db)):
    allocation = deallocate_asset_from_portfolio(db=db, allocation_id=allocation_id)
    if not allocation or not allocation.is_allocated:
        raise HTTPException(status_code=404, detail="Allocation not found or already deallocated")
    return allocation


# GET : Retrieve all the allocations for a portfolio
@router.get("/portfolioAllocations/{portfolio_id}/", response_model=list[PortfolioAssetAllocation])
def get_portfolio_allocations(
    portfolio_id: int,  
    StartDate: date,
    EndDate: date,
    skip: int = 0,
    limit: int = 100, 
    db: Session = Depends(get_db)):

    allocations = get_allocations_portfolio(db=db, portfolio_id=portfolio_id, startDate=StartDate, endDate=EndDate, skip=skip, limit=limit)
    if not allocations:
        raise HTTPException(status_code=404, detail="Allocations not found")
    return allocations


#GET : Retrieve all the allocations
@router.get("/allocations", response_model=list[PortfolioAssetAllocation])
def get_allocations_time_range(
    StartDate: date,
    EndDate: date,
    skip: int = 0,
    limit: int = 100, 
    db: Session = Depends(get_db)):

    allocations = get_allocations(db=db, startDate=StartDate, endDate=EndDate, skip=skip, limit=limit)
    if not allocations:
        raise HTTPException(status_code=404, detail="Allocations not found")
    return allocations