# Improving Data Quality and Detecting Anomalies in Financial Transactions (AML Use Case)

## Project Overview  
This case study simulates the responsibilities of an **Information Management Analyst** working in the financial sector.  
The focus is on **data quality assessment, metadata management, and anomaly detection** in transaction data to support **AML (Anti-Money Laundering) compliance**.  

**Dataset**: [PaySim Synthetic Financial Dataset](https://www.kaggle.com/datasets/ealaxi/paysim1)  
- ~6M financial transactions  
- Features: transaction type, amount, customer IDs, old/new balances, fraud labels  

---

## Business Problem  
Financial institutions must ensure **data quality, transparency, and fraud detection** to comply with AML regulations.  
Poor-quality data increases compliance risks and reduces fraud monitoring effectiveness.  

This project explores how to:  
- Assess and improve **data quality** (cleaning, validation, metadata management).  
- Detect **anomalous transactions** using SQL and Python.  
- Visualize fraud detection trends for better **compliance monitoring**.  

---

## Approach  

### 1. Data Quality Assessment & Metadata Management  
- Checked for missing, duplicate, and inconsistent values.  
- Created **metadata summary tables** for transaction types, amounts, and IDs.  
- Applied rule-based validation (e.g., negative balances, invalid transaction flows).  

### 2. Data Cleaning & Standardization  
- Standardized transaction metadata (consistent formats, retention rules).  
- Applied SQL scripts for deduplication and anomaly flagging.  
- Logged all corrections for **audit transparency**.  

### 3. Anomaly Detection (AML Use Case)  
- **SQL Queries** → Flagged abnormal transaction patterns (e.g., unusually high amounts, rapid transfers).  
- **Python ML Models**:  
  - Isolation Forest  
  - Random Forest Classifier (baseline fraud detection)  
- Evaluated precision, recall, and F1-score.  

### 4. Visualization & Reporting  
- Built **Tableau dashboards**:  
  - Data Quality Scorecard (missing %, duplicates, invalid entries).  
  - Anomaly Detection Results (suspicious transactions by type & time).  
  - Fraud Trends Overview.  

---

## Results (to be filled in)  
- ✅ Improved data quality from **X% → Y% valid records**.  
- ✅ Anomaly detection achieved **XX% recall and XX% precision**.  
- ✅ Dashboards provided actionable insights for **compliance monitoring**.  

---

## Tech Stack  
- **BigQuery** (queries, ETL, metadata)  
- **Python (Pandas, Scikit-learn, Plotly, Dash)**  
- **Tableau** (visualization)  
- **GitHub** (documentation & version control)  

---

## Next Steps  
- Expand anomaly detection with **deep learning models** (e.g., LSTMs).  
- Add **automated data quality pipelines** with validation alerts.  
- Integrate with **real-time dashboards** for monitoring.  

---

## Repository Structure  
- dashboards/ # Tableau files or screenshots
- data/ # sample / cleaned datasets
- notebooks/ # R Markdown (exploration + modeling)
- sql/ # SQL scripts for data validation & cleaning
- README.md # project overview

## Author  
**Kinga Sligar**  
- LinkedIn: [Linkedin link](https://www.linkedin.com/in/kinga-sligar-1355441a3/?locale=en_US)  
- Portfolio: [GitHub link](https://github.com/KingaBlaszczyk0409)  
- Email: kblaszczyk0409@gmail.com 
