# schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from datetime import datetime

class InvestorCreate(BaseModel):
    Name: str
    InvestorType: str
    ContactInfo: str
    RiskTolerance: str
    AccountBalance: float

class Investor(BaseModel):
    InvestorID: int
    Name: str
    InvestorType: str
    ContactInfo: str
    RiskTolerance: str
    AccountBalance: float

    class Config:
        orm_mode = True

class PortfolioCreate(BaseModel):
    InvestorID: int
    PortfolioName: str
    PortfolioType: str
    CreationDate: date
    TotalValue: float

class Portfolio(BaseModel):
    PortfolioID: int
    InvestorID: int
    PortfolioName: str
    PortfolioType: str
    CreationDate: date
    TotalValue: float

    class Config:
        orm_mode = True

class AssetCreate(BaseModel):
    AssetName: str
    AssetType: str
    TickerSymbol: str
    CurrentPrice: float

class Asset(BaseModel):
    AssetID: int
    AssetName: str
    AssetType: str
    TickerSymbol: str
    CurrentPrice: float

    class Config:
        orm_mode = True

class TradeCreate(BaseModel):
    PortfolioID: int
    AssetID: int
    TradeType: str
    TradeDate: date
    TradePrice: float
    Quantity: int

class Trade(BaseModel):
    TradeID: int
    PortfolioID: int
    AssetID: int
    TradeType: str
    TradeDate: date
    TradePrice: float
    Quantity: int

    class Config:
        orm_mode = True

class MarketDataCreate(BaseModel):
    AssetID: int
    Date: date
    OpeningPrice: float
    ClosingPrice: float
    HighPrice: float
    LowPrice: float
    Volume: int

class MarketData(BaseModel):
    MarketDataID: int
    AssetID: int
    Date: date
    OpeningPrice: float
    ClosingPrice: float
    HighPrice: float
    LowPrice: float
    Volume: int

    class Config:
        orm_mode = True

class RiskMetricCreate(BaseModel):
    PortfolioID: Optional[int]
    AssetID: Optional[int]
    MetricName: str
    MetricValue: float
    CalculationDate: date

class RiskMetric(BaseModel):
    RiskMetricID: int
    PortfolioID: Optional[int]
    AssetID: Optional[int]
    MetricName: str
    MetricValue: float
    CalculationDate: date

    class Config:
        orm_mode = True




class PortfolioAssetAllocationBase(BaseModel):
    quantity: float
    purchase_price: float

class PortfolioAssetAllocationCreate(PortfolioAssetAllocationBase):
    pass

class PortfolioAssetAllocation(PortfolioAssetAllocationBase):
    AllocationID: int
    PortfolioID: int
    AssetID: int
    allocated_at: datetime
    valid_to: Optional[datetime] = None
    is_allocated: bool

    class Config:
        orm_mode = True


class MultipleAssetsCreate(BaseModel):
    assets: List[AssetCreate]


class MultipleInvestorsCreate(BaseModel):
    investors: List[InvestorCreate]

class MultiplePortfoliosCreate(BaseModel):
    portfolios: List[PortfolioCreate]

class MultipleTradesCreate(BaseModel):
    trades: List[TradeCreate]


class MultipleMarketDataCreate(BaseModel):
    marketdata: List[MarketDataCreate]