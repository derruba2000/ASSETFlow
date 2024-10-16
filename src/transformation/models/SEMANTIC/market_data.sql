{{ config(
            materialized='incremental',
            schema="SEMANTIC",
            unique_key=['MARKET_DATA_ID']
        ) 
}}



SELECT
    M.MARKET_DATA_ID, 
    CAST(M."DATE" AS DATE) AS MARKET_DATE, 
    M.OPENING_PRICE, 
    M.CLOSING_PRICE, 
    M.HIGH_PRICE, 
    M.LOW_PRICE, 
    M."VOLUME",
    A.PK_ASSET_ID AS PK_ASSET_ID,
FROM {{source('ASSET_FLOW_STAGING','STREAM_MARKET_DATA')}} AS M
ASOF JOIN {{ref('asset')}} AS A 
    MATCH_CONDITION(CAST(M."DATE" AS DATE)  >= A.VALID_FROM) ON A.ASSET_ID=M.ASSET_ID
{% if is_incremental() %}
WHERE MARKET_DATE >= (select coalesce(max(MARKET_DATE),'1900-01-01') from {{ this }} )
{% endif %}