{{ config(
            materialized='incremental',
            strategy="delete+insert",
            schema="SEMANTIC",
            unique_key=['PK_POSITION']
        ) 
}}


WITH CumulativeTrades AS (
    SELECT 
        t.PK_PORTFOLIO_ID,
        t.PK_ASSET_ID,
        t.TRADE_DATE,
        HASH(t.PK_PORTFOLIO_ID,
        t.PK_ASSET_ID,
        t.TRADE_DATE) AS PK_POSITION,
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
        PK_PORTFOLIO_ID,
        PK_ASSET_ID,
        TRADE_DATE,
        PK_POSITION,
        SUM(QuantityChange) OVER (PARTITION BY PK_PORTFOLIO_ID, PK_ASSET_ID ORDER BY TRADE_DATE ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS Position
    FROM 
        CumulativeTrades
)
SELECT 
    PK_PORTFOLIO_ID,
    PK_ASSET_ID,
    TRADE_DATE,
    PK_POSITION
    Position,
    CURRENT_TIMESTAMP AS created_at,
    {{"'" ~var("processid")~ "'" }} AS ProcessId
FROM 
    PositionPerDay
