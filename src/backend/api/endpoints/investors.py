# app/api/endpoints/investors.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.schemas import Investor, InvestorCreate
from crud import create_investor, get_investors, get_investor, update_investor
from database import SessionLocal

router = APIRouter()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST: Create a new investor
@router.post("/", response_model=Investor)
def create_new_investor(investor: InvestorCreate, db: Session = Depends(get_db)):
    db_investor = create_investor(db=db, investor=investor)
    return db_investor

# GET: Retrieve all investors
@router.get("/", response_model=List[Investor])
def read_investors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    investors = get_investors(db=db, skip=skip, limit=limit)
    return investors

# GET: Retrieve a specific investor by ID
@router.get("/{investor_id}", response_model=Investor)
def read_investor(investor_id: int, db: Session = Depends(get_db)):
    db_investor = get_investor(db=db, investor_id=investor_id)
    if db_investor is None:
        raise HTTPException(status_code=404, detail="Investor not found")
    return db_investor

# PUT: Update an existing investor by ID
@router.put("/{investor_id}", response_model=Investor)
def update_existing_investor(investor_id: int, investor: InvestorCreate, db: Session = Depends(get_db)):
    db_investor = update_investor(db=db, investor_id=investor_id, investor=investor)
    if db_investor is None:
        raise HTTPException(status_code=404, detail="Investor not found")
    return db_investor
