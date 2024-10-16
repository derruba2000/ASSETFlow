/*
ASSET table slow changing dimension type 2

*/

{{ config(
            materialized='incremental',
            schema="SEMANTIC",
            unique_key=['PK_ASSET_ID']
        ) 
}}

SELECT
    A.ASSET_ID, 
    A.ASSET_NAME, 
    A.ASSET_TYPE, 
    A.TICKER_SYMBOL, 
    A.CURRENT_PRICE,
    CURRENT_DATE AS VALID_FROM, 
    HASH(A.ASSET_ID, 
        A.ASSET_NAME, 
        A.ASSET_TYPE, 
        A.TICKER_SYMBOL, 
        A.CURRENT_PRICE) AS PK_ASSET_ID 
FROM {{source('ASSET_FLOW_STAGING','STREAM_ASSETS')}} AS A