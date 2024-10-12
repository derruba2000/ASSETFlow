# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date,  DateTime, func
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
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

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
