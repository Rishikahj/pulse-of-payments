# 💳 Pulse of Payments — India Digital Payment Fraud Intelligence

## 🔗 Live Dashboard
[👉 Click here to view live interactive Power BI dashboard](YOUR_POWERBI_LINK_HERE)

## 🎯 Business Problem
Indian banks and fintech companies lose thousands of crores annually to payment fraud. Fraud teams cannot manually monitor every transaction. This project builds a **Fraud Intelligence & Risk Analytics System** that identifies exactly when, where, and how fraud happens across Indian digital payment channels.

## 📊 Project Type
**Full Stack Data Analytics Project** — End-to-end pipeline from data engineering to live dashboard deployment.

## 🛠️ Tools Used
| Tool | Purpose |
|---|---|
| Python (Pandas, Matplotlib, Seaborn) | Data generation, cleaning, EDA |
| SQL (SQLite) | Advanced analytics queries |
| Power BI | 5-page interactive dashboard |
| Excel | Business report with recommendations |
| GitHub | Version control and documentation |

## 📁 Dataset
- **Type:** Synthetic Indian payment dataset engineered using Python
- **Size:** 50,000 transactions (2023–2024)
- **Columns:** transaction_id, payment_method (UPI/Credit Card/Debit Card/Net Banking/Wallet), transaction_amount, city, state, bank_provider, device_type, customer_age_group, merchant_category, hour, fraud_risk_score, fraud_label, investigation_status
- **Why synthetic:** No public Indian UPI fraud dataset exists — I engineered realistic data simulating actual Indian payment patterns

## 🔍 Key Findings
- **UPI** had the highest fraud count — most used payment method in India
- **Night hours (11PM–4AM)** showed 3x higher fraud rate than morning hours
- **Electronics and Travel** merchant categories had the highest fraud rates
- **Desktop/Laptop** devices showed higher fraud rates than mobile devices
- **Investigation funnel** revealed only a small percentage of flagged cases reach resolution — pipeline inefficiency identified

## 📁 Project Structure

```
pulse-of-payments/
├── data/
│   ├── india_payments_raw.csv      # Raw generated dataset
│   ├── india_payments_clean.csv    # Cleaned dataset
│   └── payments_india.db           # SQLite database
├── notebooks/
│   └── 01_generate_dataset.ipynb  # Python analysis notebook
├── sql/
│   └── fraud_analysis.sql          # 7 advanced SQL queries
├── outputs/
│   ├── chart1_fraud_overview.png
│   ├── chart2_investigation_funnel.png
│   ├── chart3_geographic_trends.png
│   └── Pulse_of_Payments_Business_Report.xlsx
└── powerbi/
    └── Pulse_of_Payments_Dashboard.pbix
```

## 📈 Power BI Dashboard Pages
1. **Executive Overview** — KPI cards, fraud by payment method, monthly trend
2. **Fraud Intelligence** — Fraud by hour, merchant, risk category, bank provider
3. **Geographic Risk** — State and city level fraud analysis
4. **Investigation Funnel** — Pipeline analysis showing drop-off at each stage
5. **Customer Intelligence** — Age group, device type, day of week analysis

## 🔑 SQL Highlights
- Window functions — cumulative fraud trends
- RANK() — city and bank provider risk ranking
- CASE WHEN — hour risk classification
- Moving averages — 3-month fraud trend smoothing
- Subqueries — percentage calculations

## 💡 Business Recommendations
1. Add 2-factor authentication for transactions above ₹50,000 between 11PM–4AM
2. Flag Electronics and Travel merchant transactions above ₹5,000 for review
3. Implement device-based risk scoring for Desktop/Laptop transactions
4. Create targeted awareness programs for high-risk age groups
5. Improve investigation pipeline to increase case resolution rate


