import pandas as pd
from pathlib import Path

# -----------------------------
# File paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "raw" / "job_description.csv"
OUTPUT_FILE = BASE_DIR / "data" / "cleaned_jobs.csv"


# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv(INPUT_FILE)

print("Original shape:", df.shape)


# -----------------------------
# Remove unnecessary column
# -----------------------------
df = df.drop(columns=["Unnamed: 0"], errors="ignore")


# -----------------------------
# Combine job text fields
# -----------------------------
text_columns = ["Description", "Requirement", "Requirements"]

for column in text_columns:
    df[column] = df[column].fillna("")

df["job_text"] = (
    df["Description"] + " " +
    df["Requirement"] + " " +
    df["Requirements"]
)


# -----------------------------
# Basic text cleaning
# -----------------------------
df["job_text"] = (
    df["job_text"]
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)


# -----------------------------
# Keep useful columns
# -----------------------------
df = df[["Category", "job_text"]]


# -----------------------------
# Remove empty job descriptions
# -----------------------------
df = df[df["job_text"].str.len() > 0]


# -----------------------------
# Remove duplicate jobs
# -----------------------------
df = df.drop_duplicates()


# -----------------------------
# Save cleaned dataset
# -----------------------------
df.to_csv(OUTPUT_FILE, index=False)


# -----------------------------
# Validation
# -----------------------------
print("Cleaned shape:", df.shape)
print("Missing values:")
print(df.isnull().sum())

print("\nCategory distribution:")
print(df["Category"].value_counts())

print(f"\nSaved cleaned dataset to: {OUTPUT_FILE}")

print("\nCleaning summary:")
print(f"Original records: 325")
print(f"Final records: {len(df)}")
print(f"Duplicate records removed: {325 - len(df)}")