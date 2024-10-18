{{ config(
            materialized='incremental',
            schema="SEMANTIC",
            unique_key=['TRADE_ID']
        ) 
}}

WITH CTE_TRADES AS (
    SELECT
    T.TRADE_ID,
    T.TRADE_TYPE,
    CAST(T.TRADE_DATE AS DATE) AS TRADE_DATE,
    T.TRADE_PRICE,
    T.QUANTITY,
    T.ASSET_ID,
    T.PORTFOLIO_ID
    FROM {{source('ASSET_FLOW_STAGING','STREAM_TRADES')}} AS T
    {% if is_incremental() %}
        WHERE CAST(T.TRADE_DATE AS DATE) >= (select coalesce(max(TRADE_DATE),'1900-01-01') from {{ this }} )
    {% endif %}
    QUALIFY ROW_NUMBER() OVER (PARTITION BY T.TRADE_ID ORDER BY CAST(T.TRADE_DATE AS DATE))=1
)
SELECT
    T.TRADE_ID,
    T.TRADE_TYPE,
    T.TRADE_DATE,
    T.TRADE_PRICE,
    T.QUANTITY,
    A.PK_ASSET_ID AS PK_ASSET_ID,
    P.PK_PORTFOLIO_ID,
    {{"'" ~var("processid")~ "'" }} AS ProcessId,
    CURRENT_TIMESTAMP AS created_at
FROM CTE_TRADES AS T
ASOF JOIN {{ref('asset')}} AS A 
    MATCH_CONDITION(T.TRADE_DATE  >= A.VALID_FROM) ON A.ASSET_ID=T.ASSET_ID
ASOF JOIN {{ref('portfolio')}} AS P
    MATCH_CONDITION(T.TRADE_DATE  >= P.VALID_FROM)  ON P.PORTFOLIO_ID=T.PORTFOLIO_ID
    WHERE T.TRADE_DATE IS NOT NULL
