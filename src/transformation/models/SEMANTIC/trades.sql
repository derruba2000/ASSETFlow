{{ config(
            materialized='incremental',
            schema="SEMANTIC",
            unique_key=['TRADE_ID']
        ) 
}}


SELECT
    T.TRADE_ID,
    T.TRADE_TYPE,
    CAST(T.TRADE_DATE AS DATE) AS TRADE_DATE,
    T.TRADE_PRICE,
    T.QUANTITY,
    A.PK_ASSET_ID AS PK_ASSET_ID,
    P.PK_PORTFOLIO_ID
FROM {{source('ASSET_FLOW_STAGING','STREAM_TRADES')}} AS T
ASOF JOIN {{ref('asset')}} AS A 
    MATCH_CONDITION(CAST(T.TRADE_DATE AS DATE)  >= A.VALID_FROM) ON A.ASSET_ID=T.ASSET_ID
ASOF JOIN {{ref('portfolio')}} AS P
    MATCH_CONDITION(CAST(T.TRADE_DATE AS DATE) >= P.VALID_FROM)  ON P.PORTFOLIO_ID=T.PORTFOLIO_ID
{% if is_incremental() %}
WHERE CAST(T.TRADE_DATE AS DATE) >= (select coalesce(max(TRADE_DATE),'1900-01-01') from {{ this }} )
{% endif %}