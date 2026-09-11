import pandas as pd
from pathlib import Path

# -----------------------------
# File paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

JOBS_FILE = BASE_DIR / "data" / "cleaned_jobs.csv"
SKILLS_FILE = BASE_DIR / "data" / "job_skills.csv"


# -----------------------------
# Load data
# -----------------------------
jobs = pd.read_csv(JOBS_FILE)
job_skills = pd.read_csv(SKILLS_FILE)

print("Jobs:", len(jobs))
print("Job-skill records:", len(job_skills))


# -----------------------------
# Number of jobs per category
# -----------------------------
jobs_per_category = (
    jobs.groupby("Category")
    .size()
    .reset_index(name="job_count")
    .sort_values("job_count", ascending=False)
)

print("\nJobs per category:")
print(jobs_per_category.to_string(index=False))


# -----------------------------
# Overall skill demand
# -----------------------------
skill_demand = (
    job_skills.groupby("skills")
    .size()
    .reset_index(name="job_count")
    .sort_values("job_count", ascending=False)
)

print("\nTop 20 skills:")
print(skill_demand.head(20).to_string(index=False))


# -----------------------------
# Skill demand by category
# -----------------------------
category_skill_demand = (
    job_skills.groupby(["Category", "skills"])
    .size()
    .reset_index(name="job_count")
    .sort_values(
        ["Category", "job_count"],
        ascending=[True, False]
    )
)

print("\nTop skills by category:")

for category in jobs["Category"].unique():
    print(f"\n{category}")

    result = category_skill_demand[
        category_skill_demand["Category"] == category
    ].head(5)

    print(result[["skills", "job_count"]].to_string(index=False))


# -----------------------------
# Skill percentage by category
# -----------------------------
category_totals = (
    jobs.groupby("Category")
    .size()
    .reset_index(name="total_jobs")
)

category_skill_percentage = category_skill_demand.merge(
    category_totals,
    on="Category"
)

category_skill_percentage["percentage"] = (
    category_skill_percentage["job_count"]
    / category_skill_percentage["total_jobs"]
    * 100
).round(2)

print("\nSkill percentages by category:")
print(
    category_skill_percentage
    .sort_values(
        ["Category", "percentage"],
        ascending=[True, False]
    )
    .head(30)
    .to_string(index=False)
)


# -----------------------------
# Transferable skills
# -----------------------------
transferable_skills = (
    job_skills.groupby("skills")["Category"]
    .nunique()
    .reset_index(name="categories_count")
    .sort_values(
        ["categories_count", "skills"],
        ascending=[False, True]
    )
)

print("\nMost transferable skills:")
print(transferable_skills.head(20).to_string(index=False))


# -----------------------------
# Save analysis outputs
# -----------------------------
skill_demand.to_csv(
    BASE_DIR / "data" / "skill_demand.csv",
    index=False
)

category_skill_percentage.to_csv(
    BASE_DIR / "data" / "category_skill_demand.csv",
    index=False
)

transferable_skills.to_csv(
    BASE_DIR / "data" / "transferable_skills.csv",
    index=False
)

print("\nAnalysis files saved successfully.")