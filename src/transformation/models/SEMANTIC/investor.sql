/*
INVESTOR table slow changing dimension type 2

*/

{{ config(
            materialized='incremental',
            schema="SEMANTIC",
            unique_key=['PK_INVESTOR_ID']
        ) 
}}

SELECT
    P.INVESTOR_ID, 
    P.NAME,
    P.INVESTOR_TYPE,
    P.CONTACT_INFO,
    P.RISK_TOLERANCE,
    P.ACCOUNT_BALANCE,
    CURRENT_DATE AS VALID_FROM, 
    HASH(P.INVESTOR_ID, 
         P.NAME,
         P.INVESTOR_TYPE,
         P.CONTACT_INFO,
         P.RISK_TOLERANCE,
         P.ACCOUNT_BALANCE) AS PK_INVESTOR_ID 
FROM {{source('ASSET_FLOW_STAGING','STREAM_INVESTORS')}} AS P