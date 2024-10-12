DROP TABLE IF EXISTS assets;
DROP TABLE IF EXISTS investors;
DROP TABLE IF EXISTS marketdata;
DROP TABLE IF EXISTS portfolios;
DROP TABLE IF EXISTS riskmetrics;
DROP TABLE IF EXISTS trades;

-- assets definition

CREATE  TABLE assets (
	"AssetID" INTEGER NOT NULL, 
	"AssetName" VARCHAR, 
	"AssetType" VARCHAR, 
	"TickerSymbol" VARCHAR, 
	"CurrentPrice" FLOAT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
	created_at  DEFAULT CURRENT_TIMESTAMP,
	updated_at  DEFAULT CURRENT_TIMESTAMP,
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
	created_at  DEFAULT CURRENT_TIMESTAMP,
	updated_at  DEFAULT CURRENT_TIMESTAMP,
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
	created_at  DEFAULT CURRENT_TIMESTAMP,
	updated_at  DEFAULT CURRENT_TIMESTAMP,
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
	created_at  DEFAULT CURRENT_TIMESTAMP,
	updated_at  DEFAULT CURRENT_TIMESTAMP,
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
	created_at  DEFAULT CURRENT_TIMESTAMP,
	updated_at  DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY ("TradeID"), 
	FOREIGN KEY("PortfolioID") REFERENCES portfolios ("PortfolioID"), 
	FOREIGN KEY("AssetID") REFERENCES assets ("AssetID")
);

CREATE INDEX "ix_trades_TradeID" ON trades ("TradeID");