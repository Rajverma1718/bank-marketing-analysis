-- Load outputs/campaign_customer_metrics.csv into a table named campaign_customer_metrics.

-- 1. Overall conversion rate
SELECT subscribed, COUNT(*) AS contacts,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS share_pct
FROM campaign_customer_metrics
GROUP BY subscribed;

-- 2. Conversion by customer segment
SELECT job, age_group, COUNT(*) AS contacts,
       ROUND(100.0 * AVG(CASE WHEN subscribed = 'yes' THEN 1.0 ELSE 0.0 END), 2) AS conversion_rate_pct
FROM campaign_customer_metrics
GROUP BY job, age_group
HAVING COUNT(*) >= 100
ORDER BY conversion_rate_pct DESC;

-- 3. Conversion by contact method
SELECT contact, COUNT(*) AS contacts,
       ROUND(100.0 * AVG(CASE WHEN subscribed = 'yes' THEN 1.0 ELSE 0.0 END), 2) AS conversion_rate_pct
FROM campaign_customer_metrics
GROUP BY contact
ORDER BY conversion_rate_pct DESC;

-- 4. Contact frequency and conversion
SELECT campaign_contacts, COUNT(*) AS contacts,
       ROUND(100.0 * AVG(CASE WHEN subscribed = 'yes' THEN 1.0 ELSE 0.0 END), 2) AS conversion_rate_pct
FROM campaign_customer_metrics
GROUP BY campaign_contacts
ORDER BY campaign_contacts;
