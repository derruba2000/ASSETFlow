{{ config(
            materialized='incremental',
            strategy="delete+insert",
            schema="SEMANTIC",
            unique_key=['PK_PORTFOLIO_ID','market_Date']
        ) 
}}

WITH CumulativeTrades AS (
    SELECT 
        t.PK_PORTFOLIO_ID,
        t.PK_ASSET_ID,
        t.TRADE_DATE,
        CASE 
            WHEN t.Trade_Type = 'Buy' THEN t.Quantity
            WHEN t.Trade_Type = 'Sell' THEN -t.Quantity
        END AS QuantityChange
    FROM 
         {{ref('trades')}} t
    {% if is_incremental() %}
        WHERE T.TRADE_DATE  >= (select coalesce(max(TRADE_DATE),'1900-01-01') from {{ this }} )
    {% endif %}
),
PositionPerDay AS (
    SELECT
        t.PK_PORTFOLIO_ID,
        t.PK_ASSET_ID,
        SUM(QuantityChange) OVER (PARTITION BY t.PK_PORTFOLIO_ID, t.PK_ASSET_ID ORDER BY t.Trade_Date) AS Position,
        m.market_Date,
        m.Closing_Price
    FROM 
        CumulativeTrades t
    INNER JOIN 
        {{ref('market_data')}} m ON t.PK_ASSET_ID = m.PK_ASSET_ID AND t.Trade_Date <= m.MARKET_Date
),
PortfolioValuePerDay AS (
    SELECT
        PK_PORTFOLIO_ID,
        market_Date,
        SUM(Position * Closing_Price) AS PortfolioValue
    FROM 
        PositionPerDay
    GROUP BY 
        ALL
)
SELECT 
    PK_PORTFOLIO_ID,
        market_Date,
    PortfolioValue,
    CURRENT_TIMESTAMP AS created_at,
    {{"'" ~var("processid")~ "'" }} AS ProcessId
FROM 
    PortfolioValuePerDay
