SELECT

    observation_date,

    con_treat,

    COUNT(*) AS users,

    SUM(converted) AS conversions,

    ROUND(AVG(converted),4) AS conversion_rate

FROM experiment

GROUP BY

    observation_date,

    con_treat

ORDER BY

    observation_date;