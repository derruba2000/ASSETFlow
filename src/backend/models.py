# models.py
from sqlalchemy import Column, Integer, Boolean, String, Float, ForeignKey, Date,  DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class Investor(Base):
    __tablename__ = "investors"
    InvestorID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Name = Column(String, index=True)
    InvestorType = Column(String)
    ContactInfo = Column(String)
    RiskTolerance = Column(String)
    AccountBalance = Column(Float)

    is_active = Column(Boolean, default=True)  # Default to active
    inactive_at = Column(DateTime, nullable=True) 
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

class Portfolio(Base):
    __tablename__ = "portfolios"
    PortfolioID = Column(Integer, primary_key=True, index=True)
    InvestorID = Column(Integer, ForeignKey("investors.InvestorID"))
    PortfolioName = Column(String)
    PortfolioType = Column(String)
    CreationDate = Column(Date)
    TotalValue = Column(Float)
    is_active = Column(Boolean, default=True)  # Default to active
    inactive_at = Column(DateTime, nullable=True) 
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    # Relationship to the allocation table
    allocations = relationship("PortfolioAssetAllocation", back_populates="portfolio")
    investor = relationship("Investor")

class Asset(Base):
    __tablename__ = "assets"
    AssetID = Column(Integer, primary_key=True, index=True)
    AssetName = Column(String)
    AssetType = Column(String)
    TickerSymbol = Column(String)
    CurrentPrice = Column(Float)
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    # Relationship to the allocation table
    allocations = relationship("PortfolioAssetAllocation", back_populates="asset")

class Trade(Base):
    __tablename__ = "trades"
    TradeID = Column(Integer, primary_key=True, index=True)
    PortfolioID = Column(Integer, ForeignKey("portfolios.PortfolioID"))
    AssetID = Column(Integer, ForeignKey("assets.AssetID"))
    TradeType = Column(String)
    TradeDate = Column(Date)
    TradePrice = Column(Float)
    Quantity = Column(Integer)
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    portfolio = relationship("Portfolio")
    asset = relationship("Asset")

class MarketData(Base):
    __tablename__ = "marketdata"
    MarketDataID = Column(Integer, primary_key=True, index=True)
    AssetID = Column(Integer, ForeignKey("assets.AssetID"))
    Date = Column(Date)
    OpeningPrice = Column(Float)
    ClosingPrice = Column(Float)
    HighPrice = Column(Float)
    LowPrice = Column(Float)
    Volume = Column(Integer)
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    asset = relationship("Asset")

class RiskMetric(Base):
    __tablename__ = "riskmetrics"
    RiskMetricID = Column(Integer, primary_key=True, index=True)
    PortfolioID = Column(Integer, ForeignKey("portfolios.PortfolioID"), nullable=True)
    AssetID = Column(Integer, ForeignKey("assets.AssetID"), nullable=True)
    MetricName = Column(String)
    MetricValue = Column(Float)
    CalculationDate = Column(Date)
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    portfolio = relationship("Portfolio", foreign_keys=[PortfolioID])
    asset = relationship("Asset", foreign_keys=[AssetID])



class PortfolioAssetAllocation(Base):
    __tablename__ = "portfolio_asset_allocations"

    AllocationID = Column(Integer, primary_key=True, autoincrement=True)
    PortfolioID = Column(Integer, ForeignKey("portfolios.PortfolioID"), nullable=False)
    AssetID = Column(Integer, ForeignKey("assets.AssetID"), nullable=False)
    quantity = Column(Float, nullable=False)  # Quantity of the asset allocated to the portfolio
    purchase_price = Column(Float, nullable=False)  # Purchase price of the asset
    allocated_at = Column(DateTime, default=func.now(), nullable=False)  # Allocation timestamp
    valid_to = Column(DateTime, nullable=True)  # Date when allocation is invalidated
    is_allocated = Column(Boolean, default=True, nullable=False)  # Allocation state (True if active)

    # Relationships (optional, but useful for easier navigation)
    portfolio = relationship("Portfolio", back_populates="allocations")
    asset = relationship("Asset", back_populates="allocations")