DROP TABLE IF EXISTS assets;
DROP TABLE IF EXISTS investors;
DROP TABLE IF EXISTS marketdata;
DROP TABLE IF EXISTS portfolio_asset_allocations;
DROP TABLE IF EXISTS portfolios;
DROP TABLE IF EXISTS riskmetrics;
DROP TABLE IF EXISTS trades;


-- assets definition

CREATE TABLE assets (
	"AssetID" INTEGER NOT NULL, 
	"AssetName" VARCHAR, 
	"AssetType" VARCHAR, 
	"TickerSymbol" VARCHAR, 
	"CurrentPrice" FLOAT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY ("AssetID")
);

CREATE INDEX "ix_assets_AssetID" ON assets ("AssetID");


-- investors definition

CREATE TABLE investors (
	"InvestorID" INTEGER NOT NULL, 
	"Name" VARCHAR, 
	"InvestorType" VARCHAR, 
	"ContactInfo" VARCHAR, 
	"RiskTolerance" VARCHAR, 
	"AccountBalance" FLOAT, 
	is_active BOOLEAN, 
	inactive_at DATETIME, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY ("InvestorID")
);

CREATE INDEX "ix_investors_InvestorID" ON investors ("InvestorID");
CREATE INDEX "ix_investors_Name" ON investors ("Name");


-- marketdata definition

CREATE TABLE marketdata (
	"MarketDataID" INTEGER NOT NULL, 
	"AssetID" INTEGER, 
	"Date" DATE, 
	"OpeningPrice" FLOAT, 
	"ClosingPrice" FLOAT, 
	"HighPrice" FLOAT, 
	"LowPrice" FLOAT, 
	"Volume" INTEGER, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY ("MarketDataID"), 
	FOREIGN KEY("AssetID") REFERENCES assets ("AssetID")
);

CREATE INDEX "ix_marketdata_MarketDataID" ON marketdata ("MarketDataID");


-- portfolios definition

CREATE TABLE portfolios (
	"PortfolioID" INTEGER NOT NULL, 
	"InvestorID" INTEGER, 
	"PortfolioName" VARCHAR, 
	"PortfolioType" VARCHAR, 
	"CreationDate" DATE, 
	"TotalValue" FLOAT, 
	is_active BOOLEAN, 
	inactive_at DATETIME, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY ("PortfolioID"), 
	FOREIGN KEY("InvestorID") REFERENCES investors ("InvestorID")
);

CREATE INDEX "ix_portfolios_PortfolioID" ON portfolios ("PortfolioID");


-- riskmetrics definition

CREATE TABLE riskmetrics (
	"RiskMetricID" INTEGER NOT NULL, 
	"PortfolioID" INTEGER, 
	"AssetID" INTEGER, 
	"MetricName" VARCHAR, 
	"MetricValue" FLOAT, 
	"CalculationDate" DATE, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY ("RiskMetricID"), 
	FOREIGN KEY("PortfolioID") REFERENCES portfolios ("PortfolioID"), 
	FOREIGN KEY("AssetID") REFERENCES assets ("AssetID")
);

CREATE INDEX "ix_riskmetrics_RiskMetricID" ON riskmetrics ("RiskMetricID");


-- trades definition

CREATE TABLE trades (
	"TradeID" INTEGER NOT NULL, 
	"PortfolioID" INTEGER, 
	"AssetID" INTEGER, 
	"TradeType" VARCHAR, 
	"TradeDate" DATE, 
	"TradePrice" FLOAT, 
	"Quantity" INTEGER, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY ("TradeID"), 
	FOREIGN KEY("PortfolioID") REFERENCES portfolios ("PortfolioID"), 
	FOREIGN KEY("AssetID") REFERENCES assets ("AssetID")
);

CREATE INDEX "ix_trades_TradeID" ON trades ("TradeID");


-- portfolio_asset_allocations definition

CREATE TABLE portfolio_asset_allocations (
	"AllocationID" INTEGER NOT NULL, 
	"PortfolioID" INTEGER NOT NULL, 
	"AssetID" INTEGER NOT NULL, 
	quantity FLOAT NOT NULL, 
	purchase_price FLOAT NOT NULL, 
	allocated_at DATETIME NOT NULL, 
	valid_to DATETIME, 
	is_allocated BOOLEAN NOT NULL, 
	PRIMARY KEY ("AllocationID"), 
	FOREIGN KEY("PortfolioID") REFERENCES portfolios ("PortfolioID"), 
	FOREIGN KEY("AssetID") REFERENCES assets ("AssetID")
);