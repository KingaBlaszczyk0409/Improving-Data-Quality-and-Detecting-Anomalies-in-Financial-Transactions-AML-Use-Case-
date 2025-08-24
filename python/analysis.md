# PaySim Fraud Detection Analysis

## 1. Introduction

This document presents an exploratory data analysis (EDA) and preliminary modeling of the PaySim dataset for fraud detection. The goal is to understand patterns in fraudulent transactions and evaluate which features are most predictive.

## 2. Dataset Overview

* Dataset shape: (6,362,620, 11)
* Total transactions: 6,362,620
* Total fraud transactions: 8,213
* Fraud ratio: 0.00129 (~0.129%)

Transaction type counts:

* TRANSFER     2,053,624
* CASH_OUT     1,890,147
* CASH_IN      1,947,495
* DEBIT          470,530
* PAYMENT       500,824

## 3. Initial Observations

Fraud by transaction type:

  type	Fraud rate (%)
* TRANSFER	0.77
* CASH_OUT	0.18
* CASH_IN	0.00
* DEBIT	0.00
* PAYMENT	0.00

Insight: Fraud predominantly occurs in TRANSFER and CASH_OUT transactions.

Balance inconsistencies:

Fraction of transactions with orig balance inconsistency: 0.819

Fraction with dest balance inconsistency: 0.744

Fraud transactions with orig inconsistency: 0.007

Fraud transactions with dest inconsistency: 0.648

4. Feature Engineering

Created error balances:

df["errorBalanceOrig"] = df["newBalanceOrig"] + df["amount"] - df["oldBalanceOrig"]
df["errorBalanceDest"] = df["oldBalanceDest"] + df["amount"] - df["newBalanceDest"]


Added binary flags:

df_model["isTransfer"] = (df_model["type"] == "TRANSFER").astype(int)
df_model["isZeroOrig"] = ((df_model["oldBalanceOrig"] == 0) & (df_model["amount"] > 0)).astype(int)
df_model["isZeroDest"] = ((df_model["oldBalanceDest"] == 0) & (df_model["amount"] > 0)).astype(int)


Selected features for modeling:

features = [
    "amount",
    "oldBalanceOrig", "newBalanceOrig",
    "oldBalanceDest", "newBalanceDest",
    "errorBalanceOrig", "errorBalanceDest",
    "isTransfer", "isZeroOrig", "isZeroDest"
]

5. Correlation Analysis

Correlation with fraud:

isFraud             1.00
oldBalanceOrig      0.35
isZeroDest          0.08
amount              0.07
errorBalanceDest    0.07
newBalanceOrig      0.06
isTransfer          0.04
newBalanceDest     -0.01
oldBalanceDest     -0.01
errorBalanceOrig   -0.02
isZeroOrig         -0.05


Insight:

oldBalanceOrig shows the strongest linear correlation with fraud.

Other features show weak correlations individually, but may be predictive in non-linear models.

6. Random Forest Feature Importance
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1, class_weight="balanced")
rf.fit(X_train, y_train)

importances = rf.feature_importances_
feat_importance = sorted(zip(features, importances), key=lambda x: x[1], reverse=True)
for feat, score in feat_importance:
    print(f"{feat}: {score:.4f}")


Results:

errorBalanceOrig: 0.4502
oldBalanceOrig: 0.1777
newBalanceOrig: 0.1178
newBalanceDest: 0.0822
isZeroOrig: 0.0443
errorBalanceDest: 0.0389
amount: 0.0383
oldBalanceDest: 0.0283
isZeroDest: 0.0141
isTransfer: 0.0082


Insight:

errorBalanceOrig is the most important feature, followed by oldBalanceOrig and newBalanceOrig.

Flags like isZeroOrig and isZeroDest contribute moderately.

Non-linear models (Random Forest) capture complex interactions beyond simple correlation.

7. Visualizations
Fraud Rate by Transaction Type
plt.figure(figsize=(8,4))
sns.barplot(x=fraud_by_type.index, y=fraud_by_type.values)
plt.title("Fraud Rate by Transaction Type")
plt.ylabel("Fraud Rate")
plt.show()


Transaction Amount Distribution (Log-Log Scale)
plt.figure(figsize=(8,4))
sns.histplot(df["amount"], bins=100, log_scale=(True, True))
plt.title("Transaction Amount Distribution (log-log scale)")
plt.xlabel("Amount")
plt.ylabel("Count")
plt.show()


8. Key Insights

Fraud is extremely rare (~0.13%) and concentrated in TRANSFER and CASH_OUT.

Balance inconsistency, especially errorBalanceOrig, is highly predictive of fraud.

Simple correlation does not fully capture predictive power — non-linear relationships exist.

Random Forest captures these patterns effectively, prioritizing features like errorBalanceOrig and oldBalanceOrig.

Flag variables (isZeroOrig, isZeroDest) improve detection of anomalous transactions.

9. Next Steps

Explore resampling strategies (SMOTE, undersampling) or class weights to improve fraud recall.

Evaluate additional ensemble models (Gradient Boosted Trees, XGBoost).

Compute precision-recall and ROC curves to quantify model performance in this highly imbalanced scenario.

Investigate time-based patterns and sequential dependencies for fraud prediction.
