import pandas as pd
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SKILLS_FILE = BASE_DIR / "data" / "job_skills.csv"
OUTPUT_FILE = BASE_DIR / "data" / "career_skill_profile.csv"


# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv(SKILLS_FILE)


# -----------------------------
# Number of jobs in each category
# -----------------------------
job_counts = (
    df.groupby("Category")
    .size()
    .reset_index(name="skill_mentions")
)


# -----------------------------
# Skill demand
# -----------------------------
skill_counts = (
    df.groupby(["Category", "skills"])
    .size()
    .reset_index(name="job_count")
)


# -----------------------------
# Calculate percentage
# -----------------------------
category_jobs = {
    category: len(
        df[df["Category"] == category]
    )
    for category in df["Category"].unique()
}

skill_counts["category_jobs"] = (
    skill_counts["Category"]
    .map(category_jobs)
)

skill_counts["demand_percentage"] = (
    skill_counts["job_count"]
    / skill_counts["category_jobs"]
    * 100
).round(2)


# -----------------------------
# Rank skills within category
# -----------------------------
skill_counts["rank"] = (
    skill_counts
    .groupby("Category")["demand_percentage"]
    .rank(
        method="first",
        ascending=False
    )
)


# -----------------------------
# Top 10 skills per career
# -----------------------------
top_skills = skill_counts[
    skill_counts["rank"] <= 10
].sort_values(
    ["Category", "rank"]
)


# -----------------------------
# Save
# -----------------------------
top_skills.to_csv(
    OUTPUT_FILE,
    index=False
)


# -----------------------------
# Display
# -----------------------------
for category in top_skills["Category"].unique():

    print(f"\n{'=' * 50}")
    print(category)
    print(f"{'=' * 50}")

    result = top_skills[
        top_skills["Category"] == category
    ][
        ["rank", "skills", "demand_percentage"]
    ]

    print(
        result.to_string(index=False)
    )


print(
    f"\nSaved to: {OUTPUT_FILE}"
)