# main.py
from fastapi import FastAPI, Depends
from database import SessionLocal, engine, Base

#---------------------------------------
from api.endpoints import investors, portfolios, assets, market_data, trades, portfolio_asset_allocation

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(investors.router, prefix="/investors", tags=["Investors"])
app.include_router(portfolios.router, prefix="/portfolios", tags=["Portfolios"])
app.include_router(assets.router, prefix="/assets", tags=["Assets"])
app.include_router(market_data.router, prefix="/market_data", tags=["MarketData"])
app.include_router(trades.router, prefix="/trades", tags=["Trades"])
app.include_router(portfolio_asset_allocation.router, prefix="/portfolio_asset_allocation", tags=["Portfolio Asset Allocation"])

# create a get hello world endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}