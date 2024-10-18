{{ config(
            materialized='incremental',
            schema="SEMANTIC",
            unique_key=['MARKET_DATA_ID']
        ) 
}}


WITH CTE_MARKET_DATA AS (
    SELECT
    M.MARKET_DATA_ID, 
    CAST(M."DATE" AS DATE) AS MARKET_DATE, 
    M.OPENING_PRICE, 
    M.CLOSING_PRICE, 
    M.HIGH_PRICE, 
    M.LOW_PRICE, 
    M."VOLUME",
    M.ASSET_ID,
    FROM {{source('ASSET_FLOW_STAGING','STREAM_MARKET_DATA')}} AS M
    {% if is_incremental() %}
    WHERE CAST(M."DATE" AS DATE) >= (select coalesce(max(MARKET_DATE),'1900-01-01') from {{ this }} )
    {% endif %}
    QUALIFY ROW_NUMBER() OVER (PARTITION BY M.MARKET_DATA_ID ORDER BY M."DATE")=1
)
SELECT
    M.MARKET_DATA_ID, 
    M.MARKET_DATE, 
    M.OPENING_PRICE, 
    M.CLOSING_PRICE, 
    M.HIGH_PRICE, 
    M.LOW_PRICE, 
    M."VOLUME",
    A.PK_ASSET_ID AS PK_ASSET_ID,
    CURRENT_TIMESTAMP AS CREATED_AT,
    {{"'" ~var("processid")~ "'" }} AS ProcessId
FROM CTE_MARKET_DATA AS M
ASOF JOIN {{ref('asset')}} AS A 
    MATCH_CONDITION(M.MARKET_DATE  >= A.VALID_FROM) ON A.ASSET_ID=M.ASSET_ID
    WHERE M.MARKET_DATE IS NOT NULL
