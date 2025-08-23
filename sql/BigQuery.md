# Preliminary SQL Analysis – PaySim Fraud Dataset

**Dataset Columns:**  
`step`, `type`, `amount`, `nameOrig`, `oldBalanceOrig`, `newBalanceOrig`, `nameDest`, `oldBalanceDest`, `newBalanceDest`, `isFraud`, `isFlaggedFraud`  

---

## 1. Dataset Overview

### 1.1 Total Transactions
```sql
SELECT COUNT(*) AS total_transactions
FROM transactions;
```

Insights:
Example: The dataset contains **__** total transactions._

### 1.2 Total Fraudulent Transactions
```sql
SELECT COUNT(*) AS total_fraud
FROM transactions
WHERE isFraud = 1;
```

Insights:
Example: There are **__** fraudulent transactions._

1.3 Transactions per Type
```sql
SELECT type, COUNT(*) AS total
FROM transactions
GROUP BY type
ORDER BY total DESC;
```

Insights:
(Which transaction types are most common?)

1.4 Fraudulent Transactions per Type
```sql
SELECT type, COUNT(*) AS total_fraud
FROM transactions
WHERE isFraud = 1
GROUP BY type
ORDER BY total_fraud DESC;
```

Insights:
(Which types are most fraud-prone?)

2. Descriptive Statistics
2.1 Amount Statistics (All Transactions)
```sql
SELECT 
    MIN(amount) AS min_amount,
    MAX(amount) AS max_amount,
    AVG(amount) AS avg_amount,
    SUM(amount) AS total_amount
FROM transactions;
```

Insights:
(Min, max, avg, and total amounts for all transactions)

2.2 Amount Statistics (Fraudulent Transactions)
```sql
SELECT 
    MIN(amount) AS min_amount,
    MAX(amount) AS max_amount,
    AVG(amount) AS avg_amount,
    SUM(amount) AS total_amount
FROM transactions
WHERE isFraud = 1;
```

Insights:
(Compare amounts in fraud vs. normal transactions)

2.3 Fraud Rate by Transaction Type
```sql
SELECT 
    type,
    COUNT(*) AS total,
    SUM(isFraud) AS fraud_count,
    ROUND(AVG(isFraud)*100,2) AS fraud_percentage
FROM transactions
GROUP BY type
ORDER BY fraud_percentage DESC;
```

Insights:
(Which types have the highest fraud rate?)

3. Balance Checks / Data Quality
3.1 Transactions with Zero Origin Balance but Non-Zero Amount
```sql
SELECT COUNT(*) AS zero_orig_balance
FROM transactions
WHERE oldBalanceOrig = 0 AND amount > 0;
```

Insights:
(Potential data anomaly: origin accounts starting with zero?)

3.2 Transactions with Zero Destination Balance but Non-Zero Amount
```sql
SELECT COUNT(*) AS zero_dest_balance
FROM transactions
WHERE oldBalanceDest = 0 AND amount > 0;
```

Insights:
(Potential data anomaly: destination accounts receiving money with zero balance?)

3.3 Fraudulent Transactions with Zero Destination Balance
```sql
SELECT COUNT(*) AS fraud_zero_dest
FROM transactions
WHERE isFraud = 1 AND oldBalanceDest = 0 AND newBalanceDest = 0;
```

Insights:
(Does fraud happen when destination accounts start at zero?)

4. Account-Level Analysis
4.1 Total Transactions per Origin Account
```sql
SELECT nameOrig, COUNT(*) AS total_txn, SUM(amount) AS total_amount
FROM transactions
GROUP BY nameOrig
ORDER BY total_txn DESC
LIMIT 10;
```

Insights:
(Top origin accounts by number of transactions and total amount)

4.2 Total Fraudulent Transactions per Origin Account
```sql
SELECT nameOrig, COUNT(*) AS total_fraud, SUM(amount) AS total_fraud_amount
FROM transactions
WHERE isFraud = 1
GROUP BY nameOrig
ORDER BY total_fraud DESC
LIMIT 10;
```

Insights:
(Which origin accounts have the most fraudulent transactions?)

4.3 Accounts Involved in Both TRANSFER and CASH_OUT Fraud
```sql
SELECT DISTINCT t1.nameDest AS fraud_account
FROM transactions t1
JOIN transactions t2
  ON t1.nameDest = t2.nameOrig
WHERE t1.type = 'TRANSFER' AND t1.isFraud = 1
  AND t2.type = 'CASH_OUT' AND t2.isFraud = 1;
```

Insights:
(Accounts potentially involved in multi-step fraud schemes)

5. Time-Based Analysis
5.1 Fraudulent Transactions Over Time
```sql
SELECT step, COUNT(*) AS fraud_count
FROM transactions
WHERE isFraud = 1
GROUP BY step
ORDER BY step;
```

Insights:
(Are frauds evenly distributed over time or clustered?)

5.2 Total Transactions Over Time
```sql
SELECT step, COUNT(*) AS total_txn
FROM transactions
GROUP BY step
ORDER BY step;
```

Insights:
(Compare total activity vs. fraud activity over time)
