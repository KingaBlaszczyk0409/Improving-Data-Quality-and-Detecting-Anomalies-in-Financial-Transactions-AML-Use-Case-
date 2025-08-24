import gc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Display helpers
pd.options.display.max_columns = 60
pd.options.display.float_format = "{:,.2f}".format

# 1) file path
csv_path = "data/data/PaySim_dataset.csv"

# 2) dtype suggestions to reduce memory
dtype_hint = {
    "step": "int32",
    "type": "category",
    "amount": "float64",
    "nameOrig": "string",
    "oldbalanceOrg": "float64",
    "newbalanceOrig": "float64",
    "nameDest": "string",
    "oldbalanceDest": "float64",
    "newbalanceDest": "float64",
    "isFraud": "int8",
    "isFlaggedFraud": "int8"
}

# 3) load with dtype mapping
try:
    df = pd.read_csv(csv_path, dtype=dtype_hint, low_memory=False)
except MemoryError:
    # If memory is insufficient, read in chunks and concat
    chunks = []
    for chunk in pd.read_csv(csv_path, dtype=dtype_hint, chunksize=300_000):
        chunks.append(chunk)
    df = pd.concat(chunks, ignore_index=True)
    del chunks
    gc.collect()

# 4) harmonize column names
df.columns = [c.strip() for c in df.columns]
rename_map = {
    "oldbalanceOrg": "oldBalanceOrig",
    "newbalanceOrig": "newBalanceOrig",
    "oldbalanceDest": "oldBalanceDest",
    "newbalanceDest": "newBalanceDest"
}
df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

# 5) quick sanity checks / prints
print("Shape:", df.shape)
print("\nColumns and dtypes:")
print(df.dtypes)
print("\nFirst 5 rows:")
print(df.head().T)

# 6) Basic verification counts
total_tx = len(df)
total_fraud = int(df["isFraud"].sum())
print(f"\nTotal transactions: {total_tx}")
print(f"Total fraud transactions: {total_fraud}")
print("\nTransaction type counts:")
print(df["type"].value_counts(dropna=False))

# 7) Nulls / zeros checks that are important for PaySim-style data
print("\nNull counts per column:")
print(df.isnull().sum())

# Example useful quick checks:
frac_zero_orig_balance_amt_positive = (
    ((df.get("oldBalanceOrig", df.get("oldbalanceOrg", pd.Series(0))) == 0) & (df["amount"] > 0))
).mean()
print("\nFraction rows with oldBalanceOrig == 0 AND amount > 0:", frac_zero_orig_balance_amt_positive)

frac_zero_dest_balance_amt_positive = ((df["oldBalanceDest"] == 0) & (df["amount"] > 0)).mean()
print("Fraction rows with oldBalanceDest == 0 AND amount > 0:", frac_zero_dest_balance_amt_positive)

# 8) Make a small stratified EDA-sample (keeps all fraud rows + random subset of non-fraud)
fraud_df = df[df["isFraud"] == 1]
nonfraud_df = df[df["isFraud"] == 0]
sample_nonfraud = nonfraud_df.sample(n=min(200_000, len(nonfraud_df)), random_state=42)
eda_sample = pd.concat([fraud_df, sample_nonfraud], ignore_index=True)
print("\nEDA sample saved to variable `eda_sample` with shape:", eda_sample.shape)

# Optional: persist the sample for quick plotting later
eda_sample.to_parquet("data/eda_sample.parquet", index=False)
print("EDA sample written to data/eda_sample.parquet")

# --- 1. Fraud ratio
fraud_ratio = df["isFraud"].mean()
print(f"Fraud ratio: {fraud_ratio:.5f} (~{fraud_ratio*100:.3f}%)")

# --- 2. Fraud by transaction type
fraud_by_type = df.groupby("type")["isFraud"].mean().sort_values(ascending=False)
print("\nFraud rate by type:\n", fraud_by_type)
print("\nFraud rate by type (%):\n", fraud_by_type*100)

plt.figure(figsize=(8,4))
sns.barplot(x=fraud_by_type.index, y=fraud_by_type.values)
plt.title("Fraud Rate by Transaction Type")
plt.ylabel("Fraud Rate")
plt.show()

# --- 3. Transaction amount distribution
plt.figure(figsize=(8,4))
sns.histplot(df["amount"], bins=100, log_scale=(True, True))
plt.title("Transaction Amount Distribution (log-log scale)")
plt.xlabel("Amount")
plt.ylabel("Count")
plt.show()

# --- 4. Feature engineering: error balances
df["errorBalanceOrig"] = df["newBalanceOrig"] + df["amount"] - df["oldBalanceOrig"]
df["errorBalanceDest"] = df["oldBalanceDest"] + df["amount"] - df["newBalanceDest"]

print("\nerrorBalanceOrig stats:")
print(df["errorBalanceOrig"].describe().apply(lambda x: f"{x:,.2f}"))
print("\nerrorBalanceDest stats:")
print(df["errorBalanceDest"].describe().apply(lambda x: f"{x:,.2f}"))

# --- 5. Check how many transactions have balance inconsistencies
inconsistent_orig = (df["errorBalanceOrig"] != 0).mean()
inconsistent_dest = (df["errorBalanceDest"] != 0).mean()
print(f"\nFraction with orig inconsistency: {inconsistent_orig:.3f}")
print(f"Fraction with dest inconsistency: {inconsistent_dest:.3f}")

# --- 6. How many fraud cases have inconsistencies?
fraud_inconsistent_orig = df.loc[df["isFraud"]==1, "errorBalanceOrig"].ne(0).mean()
fraud_inconsistent_dest = df.loc[df["isFraud"]==1, "errorBalanceDest"].ne(0).mean()
print(f"\nFraud rows with orig inconsistency: {fraud_inconsistent_orig:.3f}")
print(f"Fraud rows with dest inconsistency: {fraud_inconsistent_dest:.3f}")

# --- Step 3: Final cleaning + engineered features ---

# 1. Keep only TRANSFER + CASH_OUT (others have ~0 fraud)
df_model = df[df["type"].isin(["TRANSFER", "CASH_OUT"])].copy()

# 2. Encode transaction type as binary
df_model["isTransfer"] = (df_model["type"] == "TRANSFER").astype(int)

# 3. Zero-balance anomaly flags
df_model["isZeroOrig"] = ((df_model["oldBalanceOrig"] == 0) & (df_model["amount"] > 0)).astype(int)
df_model["isZeroDest"] = ((df_model["oldBalanceDest"] == 0) & (df_model["amount"] > 0)).astype(int)

# 4. Error balances (already computed in Step 2)
# Ensure they’re copied over
df_model["errorBalanceOrig"] = df["errorBalanceOrig"]
df_model["errorBalanceDest"] = df["errorBalanceDest"]

# 5. Select final feature set
features = [
    "amount",
    "oldBalanceOrig", "newBalanceOrig",
    "oldBalanceDest", "newBalanceDest",
    "errorBalanceOrig", "errorBalanceDest",
    "isTransfer", "isZeroOrig", "isZeroDest"
]

X = df_model[features]
y = df_model["isFraud"]

print("Final dataset shape:", X.shape)
print("Fraud ratio in final dataset:", y.mean())
print("Fraud ratio in final dataset (%):", y.mean()*100)

# Correlation matrix (with target)
corr = df_model[features + ["isFraud"]].corr()

plt.figure(figsize=(10,6))
plt.imshow(corr, cmap="coolwarm", interpolation="nearest")
plt.colorbar()
plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
plt.yticks(range(len(corr.columns)), corr.columns)
plt.title("Correlation Heatmap with Fraud")
plt.show()

# Print correlation with target
print("Correlation with Fraud:")
print(corr["isFraud"].sort_values(ascending=False))

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

# Simple RF
rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1, class_weight="balanced")
rf.fit(X_train, y_train)

# Feature importance
importances = rf.feature_importances_
feat_importance = sorted(zip(features, importances), key=lambda x: x[1], reverse=True)

print("Feature importance (Random Forest):")
for feat, score in feat_importance:
    print(f"{feat}: {score:.4f}")
