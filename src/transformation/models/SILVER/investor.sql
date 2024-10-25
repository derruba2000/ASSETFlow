/*
INVESTOR table slow changing dimension type 2

*/

{{ config(
            materialized='incremental',
            schema="INVESTMENT_MANAGEMENT",
            database="SILVER",
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
    {% if is_incremental() %}
        CURRENT_DATE AS VALID_FROM, 
    {% else %}
        CAST('2000-01-01' AS DATE) AS VALID_FROM, 
    {% endif %}
    HASH(P.INVESTOR_ID, 
         P.NAME,
         P.INVESTOR_TYPE,
         P.CONTACT_INFO,
         P.RISK_TOLERANCE,
         P.ACCOUNT_BALANCE) AS PK_INVESTOR_ID,
    {{"'" ~var("processid")~ "'" }} AS ProcessId
FROM {{source('BRONZE_ASSET_FLOW','STREAM_INVESTORS')}} AS P