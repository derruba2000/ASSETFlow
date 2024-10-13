# app/api/endpoints/Portfolios.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas import Portfolio, PortfolioCreate
from crud.crudPortfolio import create_portfolio, get_portfolios, get_portfolio, update_portfolio, deactivate_portfolio
from database import SessionLocal

router = APIRouter()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST: Create a new Portfolio
@router.post("/", response_model=Portfolio)
def create_new_Portfolio(portfolio: PortfolioCreate, db: Session = Depends(get_db)):
    db_Portfolio = create_portfolio(db=db, portfolio=portfolio)
    return db_Portfolio

# GET: Retrieve all Portfolios
@router.get("/", response_model=List[Portfolio])
def read_Portfolios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    Portfolios = get_portfolios(db=db, skip=skip, limit=limit)
    return Portfolios

# GET: Retrieve a specific Portfolio by ID
@router.get("/{portfolio_id}", response_model=Portfolio)
def read_Portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    db_Portfolio = get_portfolio(db=db, portfolio_id=portfolio_id)
    if db_Portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return db_Portfolio

# PUT: Update an existing Portfolio by ID
@router.put("/{portfolio_id}", response_model=Portfolio)
def update_existing_Portfolio(portfolio_id: int, Portfolio: PortfolioCreate, db: Session = Depends(get_db)):
    db_Portfolio = update_portfolio(db=db, portfolio_id=portfolio_id, Portfolio=Portfolio)
    if db_Portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return db_Portfolio


# PUT: Deactivate an Portfolio (soft delete)
@router.put("/deactivate/{portfolio_id}", response_model=Portfolio)
def deactivate_Portfolio_endpoint(portfolio_id: int, db: Session = Depends(get_db)):
    db_Portfolio = get_portfolio(db=db, portfolio_id=portfolio_id)
    if db_Portfolio is None or not db_Portfolio.is_active:
        raise HTTPException(status_code=404, detail="Portfolio not found or already inactive")
    
    deactivated_Portfolio = deactivate_portfolio(db=db, portfolio_id=portfolio_id)
    return deactivated_Portfolio