import pandas as pd
import re

# detect file type
def detect_type(df):
    cols = [c.lower() for c in df.columns]
    if "debit amount" in cols or "credit amount" in cols:
        return "GL"
    elif "vendor id" in cols:
        return "PL"
    elif "customer id" in cols:
        return "SL"
    elif "gst number" in cols:
        return "VTR"
    elif "approval status" in cols:
        return "IR"
    else:
        return "UNKNOWN"

# simple cleaning
def clean_data(df):
    # remove blank rows
    df = df.dropna(how="all")
    # strip spaces
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip()
    # convert amounts
    for col in df.columns:
        if "amount" in col.lower():
            df[col] = df[col].astype(str).str.replace(",", "")
            df[col] = df[col].str.replace("₹", "")
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

# GL rules
def process_gl(df):

    if "Journal Entry Number" in df.columns:
        df = df.drop_duplicates(subset=["Journal Entry Number"])
    if "Debit Amount" in df.columns and "Credit Amount" in df.columns:
        df["flag"] = ""
        mask = (df["Debit Amount"] > 0) & (df["Credit Amount"] > 0)
        df.loc[mask, "flag"] = "Both debit and credit filled"

    return df

# PL rules
def process_pl(df):
    if "Invoice Number" in df.columns:
        df = df.drop_duplicates(subset=["Invoice Number"])
    if "Vendor Name" in df.columns:
        df["Vendor Name"] = df["Vendor Name"].str.title()
    return df

# main runner
def run_agent1(file_path):
    df = pd.read_csv(file_path)
    print("Rows before cleaning:", len(df))

    file_type = detect_type(df)
    print("Detected file type:", file_type)
    df = clean_data(df)
    if file_type == "GL":
        df = process_gl(df)
    elif file_type == "PL":
        df = process_pl(df)
    print("Rows after cleaning:", len(df))
    return df

# example run
cleaned1 = run_agent1("purchase_ledger.csv")
cleaned2 = run_agent1("sales_ledger.csv")
print(cleaned1.head())
print("\n")
print(cleaned2.head())