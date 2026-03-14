import pandas as pd

# simple risk scoring
def risk_score(df, file_type):

    df["risk_score"] = 0
    df["risk_reason"] = ""

    # PURCHASE LEDGER RULES
    if file_type == "PL":

        # round number amounts
        if "Invoice Amount" in df.columns:
            mask = df["Invoice Amount"] % 1000 == 0
            df.loc[mask, "risk_score"] += 40
            df.loc[mask, "risk_reason"] += "Round number amount; "

        # amounts close to approval threshold
        mask = (df["Invoice Amount"] >= 95000) & (df["Invoice Amount"] < 100000)
        df.loc[mask, "risk_score"] += 80
        df.loc[mask, "risk_reason"] += "Near approval threshold; "

    # SALES LEDGER RULES
    if file_type == "SL":

        if "Invoice Date" in df.columns and "Collection Date" in df.columns:
            inv = pd.to_datetime(df["Invoice Date"], errors="coerce")
            coll = pd.to_datetime(df["Collection Date"], errors="coerce")

            mask = coll < inv
            df.loc[mask, "risk_score"] += 90
            df.loc[mask, "risk_reason"] += "Collection before invoice; "

    # GENERAL LEDGER RULES
    if file_type == "GL":

        if "Debit Amount" in df.columns and "Credit Amount" in df.columns:
            mask = (df["Debit Amount"] > 0) & (df["Credit Amount"] > 0)
            df.loc[mask, "risk_score"] += 85
            df.loc[mask, "risk_reason"] += "Debit and credit both filled; "
    return df

# assign risk band
def assign_band(df):
    bands = []

    for score in df["risk_score"]:

        if score <= 30:
            bands.append("Green")

        elif score <= 65:
            bands.append("Amber")

        else:
            bands.append("Red")

    df["risk_band"] = bands
    return df

# main runner
def run_agent2(file_path, file_type):
    df = pd.read_csv(file_path)
    print("Rows loaded:", len(df))
    print("Running risk detection for:", file_type)
    df = risk_score(df, file_type)
    df = assign_band(df)
    print("\nRisk summary")
    print(df["risk_band"].value_counts())

    return df

# example run
result1 = run_agent2("purchase_ledger.csv", "PL")
result2 = run_agent2("sales_ledger.csv", "SL")

print("\nSample output:")
print("\n=== Agent 2 Risk Analysis ===")
print("\n=== Flagged Transactions ===")
print(result1.head())

print("\nSample output:")
print("\n=== Agent 2 Risk Analysis ===")
print("\n=== Flagged Transactions ===")
print(result2.head())
