# Improving Data Quality and Detecting Anomalies in Financial Transactions (AML Use Case)

## Project Overview  
This case study simulates the responsibilities of an **Information Management Analyst** in the financial sector, focusing on data quality, feature engineering, and fraud detection.
The analysis uses the PaySim synthetic dataset to illustrate anomaly detection in financial transactions, supporting AML (Anti-Money Laundering) compliance.

**Dataset**: [PaySim Synthetic Financial Dataset](https://www.kaggle.com/datasets/ealaxi/paysim1)  
- ~6M financial transactions  
- Features: transaction type, amount, customer IDs, old/new balances, fraud labels  

---

## Business Problem  
Financial institutions need to maintain high-quality transaction data for effective fraud monitoring and AML compliance.
Poor-quality data or undetected anomalies can increase regulatory risks and reduce the effectiveness of fraud detection systems.

This project explores how to:  
- Assess and improve data quality (cleaning, validation, metadata management).
- Detect anomalous transactions using SQL and Python.
- Visualize fraud detection trends for better compliance monitoring.

---

## Approach  

### 1. Data Quality Assessment & Metadata Management
- Checked for missing, duplicate, and inconsistent values.
- Created metadata summary tables for transaction types, amounts, and customer IDs.
- Applied rule-based validation using SQL and Python:
  - Negative balances
  - Invalid transaction flows
  - Zero-balance origin/destination with positive amounts

### 2. SQL-Based Anomaly Detection
- Used SQL queries to identify suspicious transactions:
  - Transactions exceeding typical amount thresholds
  - Rapid transfers between accounts
  - Imbalances between origin and destination accounts
- Generated fraud-related statistics and aggregates:
  - Fraud counts by transaction type
  - Fractions of transactions with balance inconsistencies
  - Features like isZeroOrig and isZeroDest for anomaly flags
- These SQL-based rules informed feature engineering for Python models-Used SQL queries to identify suspicious transactions:

### 3. Python Analysis & Machine Learning 
- **Exploratory Data Analysis (EDA):**
  - Visualized transaction distributions, fraud ratios, and type breakdowns
  - Assessed balance errors (errorBalanceOrig / errorBalanceDest) and inconsistencies
- **Feature Engineering:**
  - Binary flags (isTransfer, isZeroOrig, isZeroDest)
  - Error balances to capture anomalies in transaction flows
- **Modeling:**
  - Random Forest Classifier as baseline fraud detection
  - Evaluated feature importance: error balances and origin balance were the most predictive
  - Calculated correlation matrix with fraud target
- **Results from Python Analysis:**
  - Fraud ratio: ~0.129%
  - Most fraudulent transactions: TRANSFER (~0.77% fraud)
  - Feature importance highlights:
    - errorBalanceOrig (0.45)
    - oldBalanceOrig (0.18)
    - newBalanceOrig (0.12)

### 4. Visualization & Reporting  
- Plotted fraud rate by transaction type and transaction amount distributions
- Correlation heatmaps to identify predictive features
- Optionally, Python outputs can feed into dashboards for fraud monitoring

---

## Results
- ✅ Detected fraud patterns with SQL and Python analysis
- ✅ Identified key predictive features for machine learning models
- ✅ Highlighted data quality issues and balance inconsistencies that contribute to anomalous transactions
- ✅ Produced visual insights for AML compliance monitoring 

---

## Tech Stack  
- **SQL / BigQuery** → Rule-based anomaly detection, metadata aggregation
- **Python (Pandas, Scikit-learn, Matplotlib, Seaborn)** → EDA, feature engineering, modeling
- **Parquet / CSV** → Efficient storage of EDA sample
- **Tableau / Plotly / Dash (optional)** → Dashboard visualization
- **GitHub** → Documentation & version control

---

## Next Steps  
- Expand anomaly detection with deep learning models (e.g., LSTM for sequential transaction analysis)
- Add automated data quality pipelines with validation alerts
- Integrate results into real-time dashboards for proactive monitoring

---

## Repository Structure  
```
Improving-Data-Quality-and-Detecting-Anomalies-in-Financial-Transactions-AML-Use-Case-/
│
├── dashboards/                # Tableau dashboards (screenshots)
│
├── data/                      # Sample dataset
│   └── PaySim_dataset_1_1.csv # Synthetic dataset used for AML fraud detection analysis
│
├── python/                    # Python notebooks
│   └── analysis.md             # Notes and explanations of Python-based analysis
│   └── images/                 # Visualization outputs from SQL queries
│       ├── Fraud_Rate_by_Transaction_Type.png                   # Chart: Fraudulent rate by type
│       └── Fraud_Rate_by_Transaction_Type_Log-Log_Scale.png     # Chart: Fraudulent rate by type (Log-Log Scale)
│
├── sql/                       # SQL scripts and related resources
│   ├── BigQuery.md             # SQL queries for data validation and analysis
│   └── images/                 # Visualization outputs from SQL queries
│       ├── fraud_count_by_step.png   # Chart: Fraudulent transactions over time
│       └── total_txn_by_step.png     # Chart: Total transactions over time
│
└── README.md                  # Project overview, objectives, and usage instructions        
```


## Author  
**Kinga Sligar**  
- LinkedIn: [Linkedin link](https://www.linkedin.com/in/kinga-sligar-1355441a3/?locale=en_US)  
- Portfolio: [GitHub link](https://github.com/KingaBlaszczyk0409)  
- Email: kblaszczyk0409@gmail.com 
