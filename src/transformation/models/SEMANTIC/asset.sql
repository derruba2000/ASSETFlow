/*
ASSET table slow changing dimension type 2

*/

{{ config(
            materialized='incremental',
            incremental_strategy="merge",
            pre_hook="alter session set query_tag='elt|asset'",
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
     {% if is_incremental() %}
        CURRENT_DATE AS VALID_FROM, 
    {% else %}
        CAST('2000-01-01' AS DATE) AS VALID_FROM, 
    {% endif %}
      HASH(A.ASSET_ID, 
        A.ASSET_NAME, 
        A.ASSET_TYPE, 
        A.TICKER_SYMBOL, 
        A.CURRENT_PRICE) AS PK_ASSET_ID,
    {{"'" ~var("processid")~ "'" }} AS ProcessId
FROM {{source('ASSET_FLOW_STAGING','STREAM_ASSETS')}} AS A