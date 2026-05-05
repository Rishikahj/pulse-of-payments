
-- ================================================
-- PULSE OF PAYMENTS
-- India Digital Payment Fraud Intelligence
-- SQL Analysis Queries
-- ================================================

-- Query 1: Fraud Overview by Payment Method
SELECT payment_method,
       COUNT(*) as total_transactions,
       SUM(fraud_label) as fraud_count,
       ROUND(SUM(fraud_label)*100.0/COUNT(*), 2) as fraud_rate_pct,
       ROUND(AVG(transaction_amount), 2) as avg_amount
FROM transactions
GROUP BY payment_method
ORDER BY fraud_rate_pct DESC;

-- Query 2: Top High Risk Cities with RANK()
SELECT city, state,
       COUNT(*) as total,
       SUM(fraud_label) as fraud_count,
       ROUND(SUM(fraud_label)*100.0/COUNT(*), 2) as fraud_rate_pct,
       RANK() OVER (ORDER BY SUM(fraud_label) DESC) as fraud_rank
FROM transactions
GROUP BY city, state
ORDER BY fraud_count DESC
LIMIT 10;

-- Query 3: Fraud Investigation Funnel
SELECT investigation_status,
       COUNT(*) as count,
       ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM transactions), 2) as pct_of_total,
       ROUND(AVG(transaction_amount), 2) as avg_amount,
       ROUND(AVG(fraud_risk_score), 2) as avg_risk_score
FROM transactions
GROUP BY investigation_status
ORDER BY count DESC;

-- Query 4: Hourly Fraud Pattern with Running Total
SELECT hour,
       COUNT(*) as total_transactions,
       SUM(fraud_label) as fraud_count,
       ROUND(SUM(fraud_label)*100.0/COUNT(*), 3) as fraud_rate,
       SUM(SUM(fraud_label)) OVER (ORDER BY hour) as cumulative_fraud,
       CASE
           WHEN hour >= 22 OR hour <= 4 THEN 'HIGH RISK'
           WHEN hour >= 5 AND hour <= 8 THEN 'MEDIUM RISK'
           ELSE 'LOW RISK'
       END as risk_level
FROM transactions
GROUP BY hour
ORDER BY hour;

-- Query 5: Merchant Category Risk Ranking
SELECT merchant_category,
       COUNT(*) as total,
       SUM(fraud_label) as fraud_count,
       ROUND(SUM(fraud_label)*100.0/COUNT(*), 3) as fraud_rate,
       RANK() OVER (ORDER BY SUM(fraud_label)*100.0/COUNT(*) DESC) as risk_rank
FROM transactions
GROUP BY merchant_category
ORDER BY fraud_rate DESC;

-- Query 6: Monthly Fraud Trend with 3-Month Moving Average
SELECT month,
       COUNT(*) as total_transactions,
       SUM(fraud_label) as fraud_count,
       ROUND(SUM(fraud_label)*100.0/COUNT(*), 3) as fraud_rate,
       ROUND(AVG(SUM(fraud_label)*100.0/COUNT(*)) 
           OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 3) as moving_avg_3month
FROM transactions
GROUP BY month
ORDER BY month;

-- Query 7: Bank Provider Risk Intelligence
SELECT bank_provider,
       COUNT(*) as total_transactions,
       SUM(fraud_label) as fraud_count,
       ROUND(SUM(fraud_label)*100.0/COUNT(*), 3) as fraud_rate,
       ROUND(SUM(CASE WHEN fraud_label=1 THEN transaction_amount ELSE 0 END), 2) as total_fraud_amount,
       RANK() OVER (ORDER BY SUM(fraud_label) DESC) as fraud_rank
FROM transactions
GROUP BY bank_provider
ORDER BY fraud_count DESC;
