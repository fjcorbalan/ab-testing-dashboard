SELECT
    con_treat,
    COUNT(*) AS users,
    SUM(converted) AS conversions,
    ROUND(AVG(converted),4) AS conversion_rate
FROM experiment
GROUP BY con_treat;