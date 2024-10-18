SELECT *
FROM {{ ref('market_data') }}
WHERE MARKET_DATE > CURRENT_DATE 