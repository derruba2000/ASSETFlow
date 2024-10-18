{{ config(
            materialized='incremental',
            strategy="delete+insert",
            schema="SEMANTIC",
            unique_key=['PK_PORTFOLIO_ID','DAY_CLOSE'],
            tags=["fact_table"]
        ) 
}}

WITH CumulativeTrades AS (
    SELECT 
        t.PK_PORTFOLIO_ID,
        t.PK_ASSET_ID,
        LAST_DAY(t.TRADE_DATE) AS DAY_CLOSE,
        CASE 
            WHEN t.Trade_Type = 'Buy' THEN t.Quantity
            WHEN t.Trade_Type = 'Sell' THEN -t.Quantity
        END AS QuantityChange
    FROM 
        {{ref('trades')}} t
    {% if is_incremental() %}
        WHERE T.TRADE_DATE  >= (select coalesce(max(DAY_CLOSE),'1900-01-01') from {{ this }} )
    {% endif %}
),
PositionPerAsset AS (
    SELECT
        PK_PORTFOLIO_ID,
        PK_ASSET_ID,
        DAY_CLOSE,
        SUM(QuantityChange) OVER (PARTITION BY PK_PORTFOLIO_ID, PK_ASSET_ID ORDER BY DAY_CLOSE ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS Position
    FROM 
        CumulativeTrades
),
AUMPerPortfolio AS (
    SELECT 
        p.PK_PORTFOLIO_ID,
        p.PK_ASSET_ID,
        p.Position,
        m.CLOSING_PRICE,
        p.Position * m.CLOSING_PRICE AS MarketValue,
        p.DAY_CLOSE
    FROM 
        PositionPerAsset p
    INNER JOIN 
        {{ref('market_data')}} m ON p.PK_ASSET_ID = m.PK_ASSET_ID
),
AUMPerInvestor AS (
    SELECT
        po.Investor_ID,
        ap.PK_PORTFOLIO_ID,
        SUM(ap.MarketValue) AS AUM,
        ap.DAY_CLOSE
    FROM 
        AUMPerPortfolio ap
    INNER JOIN 
        {{ref('portfolio')}} po ON ap.PK_PORTFOLIO_ID = po.PK_PORTFOLIO_ID
    GROUP BY ALL
)
SELECT 
    PK_PORTFOLIO_ID,
    SUM(AUM) AS TotalAUM,
    DAY_CLOSE,
    CURRENT_TIMESTAMP AS CREATED_AT,
    {{"'" ~var("processid")~ "'" }} AS ProcessId
FROM 
    AUMPerInvestor
WHERE PK_PORTFOLIO_ID IS NOT NULL
GROUP BY 
    ALL
