import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SKILLS_FILE = BASE_DIR / "data" / "job_skills.csv"
OUTPUT_DIR = BASE_DIR / "data" / "charts"

OUTPUT_DIR.mkdir(exist_ok=True)


# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv(SKILLS_FILE)


# -----------------------------
# 1. Top 15 Skills
# -----------------------------
top_skills = (
    df["skills"]
    .value_counts()
    .head(15)
    .sort_values()
)

plt.figure(figsize=(10, 7))

top_skills.plot(kind="barh")

plt.title("Top 15 In-Demand Skills")
plt.xlabel("Number of Job Postings")
plt.ylabel("Skill")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "top_15_skills.png",
    dpi=300
)

plt.close()


# -----------------------------
# 2. Top Skills by Category
# -----------------------------
category_skill = (
    df.groupby(["Category", "skills"])
    .size()
    .reset_index(name="job_count")
)

categories = df["Category"].unique()

for category in categories:

    data = (
        category_skill[
            category_skill["Category"] == category
        ]
        .sort_values("job_count", ascending=False)
        .head(10)
        .sort_values("job_count")
    )

    plt.figure(figsize=(9, 6))

    plt.barh(
        data["skills"],
        data["job_count"]
    )

    plt.title(
        f"Top Skills — {category}"
    )

    plt.xlabel("Number of Job Postings")
    plt.ylabel("Skill")

    plt.tight_layout()

    filename = (
        category.lower()
        .replace(" ", "_")
        .replace("/", "_")
        + "_skills.png"
    )

    plt.savefig(
        OUTPUT_DIR / filename,
        dpi=300
    )

    plt.close()


# -----------------------------
# 3. Skill × Category Heatmap
# -----------------------------
pivot = pd.crosstab(
    df["skills"],
    df["Category"]
)

top_20 = (
    df["skills"]
    .value_counts()
    .head(20)
    .index
)

pivot = pivot.loc[
    pivot.index.intersection(top_20)
]

plt.figure(figsize=(12, 9))

plt.imshow(pivot, aspect="auto")

plt.xticks(
    range(len(pivot.columns)),
    pivot.columns,
    rotation=45,
    ha="right"
)

plt.yticks(
    range(len(pivot.index)),
    pivot.index
)

plt.title("Top Skills Across Job Categories")

plt.xlabel("Job Category")
plt.ylabel("Skill")

plt.colorbar(
    label="Job Postings"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "skill_category_heatmap.png",
    dpi=300
)

plt.close()


print("Charts created successfully.")

print(f"Saved to: {OUTPUT_DIR}")

# -----------------------------
# 4. Percentage Heatmap
# -----------------------------

# Count skill mentions by category
skill_counts = pd.crosstab(
    df["skills"],
    df["Category"]
)

# Number of jobs in each category
category_job_counts = (
    df.groupby("Category")
    .size()
)

# Convert counts to percentage of jobs in each category
percentage_heatmap = (
    skill_counts
    .div(category_job_counts, axis=1)
    * 100
)

# Keep top 20 overall skills
top_20_skills = (
    df["skills"]
    .value_counts()
    .head(20)
    .index
)

percentage_heatmap = percentage_heatmap.loc[
    percentage_heatmap.index.intersection(top_20_skills)
]

# Plot
plt.figure(figsize=(12, 9))

plt.imshow(
    percentage_heatmap,
    aspect="auto"
)

plt.xticks(
    range(len(percentage_heatmap.columns)),
    percentage_heatmap.columns,
    rotation=45,
    ha="right"
)

plt.yticks(
    range(len(percentage_heatmap.index)),
    percentage_heatmap.index
)

plt.title(
    "Skill Demand by Career Category (%)"
)

plt.xlabel("Job Category")
plt.ylabel("Skill")

plt.colorbar(
    label="Percentage of Job Postings"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "skill_category_percentage_heatmap.png",
    dpi=300
)

plt.close()

print(
    "Percentage heatmap created successfully."
)