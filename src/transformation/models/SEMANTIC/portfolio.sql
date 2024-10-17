/*
PORTFOLIO table slow changing dimension type 2

*/

{{ config(
            materialized='incremental',
            schema="SEMANTIC",
            unique_key=['PK_PORTFOLIO_ID']
        ) 
}}

SELECT
    P.PORTFOLIO_ID, 
    P.INVESTOR_ID,
    P.PORTFOLIO_NAME,
    P.PORTFOLIO_TYPE,
    CAST(P.CREATION_DATE AS DATE) AS CREATION_DATE,
    P.TOTAL_VALUE,
    {% if is_incremental() %}
        CURRENT_DATE AS VALID_FROM, 
    {% else %}
        CAST('2000-01-01' AS DATE) AS VALID_FROM, 
    {% endif %}
    HASH(P.PORTFOLIO_ID, 
         P.PORTFOLIO_NAME,
         P.PORTFOLIO_TYPE) AS PK_PORTFOLIO_ID ,
         {{"'" ~var("processid")~ "'" }} AS ProcessId
FROM {{source('ASSET_FLOW_STAGING','STREAM_PORTFOLIOS')}} AS P