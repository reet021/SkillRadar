import pandas as pd
import re
from pathlib import Path

# -----------------------------
# File paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "cleaned_jobs.csv"
OUTPUT_FILE = BASE_DIR / "data" / "job_skills.csv"


# -----------------------------
# Load cleaned jobs
# -----------------------------
df = pd.read_csv(INPUT_FILE)

print("Jobs loaded:", len(df))


# -----------------------------
# Skill dictionary
# -----------------------------
skills = [
    # Data & Analytics
    "Python",
    "SQL",
    "Excel",
    "Power BI",
    "Tableau",
    "R",
    "Pandas",
    "NumPy",
    "Statistics",
    "Data Analysis",
    "Data Visualization",
    "Data Science",
    "Business Intelligence",
    "ETL",
    "Data Mining",
    "Data Engineering",
    "Database",
    "Databases",

    # Machine Learning / AI
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "Natural Language Processing",
    "Artificial Intelligence",
    "AI",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "Neural Networks",
    "Computer Vision",

    # Programming
    "Java",
    "JavaScript",
    "TypeScript",
    "C++",
    "C#",
    "C",
    "HTML",
    "CSS",
    "PHP",
    "Ruby",

    # Cloud / DevOps
    "AWS",
    "Azure",
    "GCP",
    "Google Cloud",
    "Docker",
    "Kubernetes",
    "Git",
    "GitHub",
    "CI/CD",
    "DevOps",
    "Linux",
    "Terraform",
    "Cloud Computing",

    # Databases
    "PostgreSQL",
    "MySQL",
    "MongoDB",
    "Oracle",
    "SQL Server",
    "Redis",

    # Big Data
    "Spark",
    "Hadoop",
    "Kafka",
    "Big Data",

    # Business Analysis / Management
    "Business Analysis",
    "Business Analyst",
    "Requirements Gathering",
    "Requirements Analysis",
    "Requirements Management",
    "Stakeholder Management",
    "Stakeholder Engagement",
    "Project Management",
    "Process Improvement",
    "Process Mapping",
    "Agile",
    "Scrum",
    "JIRA",
    "User Stories",
    "Acceptance Criteria",
    "UAT",
    "Testing",
    "Quality Assurance",
    "Problem Solving",
    "Microsoft Office",
    "Communication",

    # UI / UX
    "UI/UX",
    "UI Design",
    "UX Design",
    "User Experience",
    "User Interface",
    "Figma",
    "Adobe XD",
    "Wireframing",
    "Prototyping",
    "Usability Testing",

    # HR
    "Recruitment",
    "Talent Acquisition",
    "Human Resources",
    "HR",
    "Employee Relations",
    "Performance Management",
    "Payroll",
    "Onboarding",
    "Training",
    "Learning and Development",
]


# -----------------------------
# Extract skills
# -----------------------------
def extract_skills(text):
    text = str(text).lower()
    found = []

    for skill in skills:
        skill_lower = skill.lower()

        # Exact word matching for very short skills
        if skill_lower in ["r", "c", "ai", "hr"]:
            pattern = r"\b" + re.escape(skill_lower) + r"\b"

            if re.search(pattern, text):
                found.append(skill)

        # Normal matching for other skills
        else:
            if skill_lower in text:
                found.append(skill)

    return found


# -----------------------------
# Apply extraction
# -----------------------------
df["skills"] = df["job_text"].apply(extract_skills)

print("Jobs with at least one skill:",
      (df["skills"].str.len() > 0).sum())



# -----------------------------
# Normalize skill names
# -----------------------------

skill_normalization = {
    "Databases": "Database",
    "AI": "Artificial Intelligence",
    "Natural Language Processing": "NLP",
    "Google Cloud": "GCP",
}

df["skills"] = df["skills"].apply(
    lambda skill_list: [
        skill_normalization.get(skill, skill)
        for skill in skill_list
    ]
)


# -----------------------------
# Convert skills to rows
# -----------------------------
df = df.explode("skills")

df = df.dropna(subset=["skills"])

df = df[["Category", "skills"]]



# -----------------------------
# Save fresh output
# -----------------------------
df.to_csv(OUTPUT_FILE, index=False)


# -----------------------------
# Validation
# -----------------------------
print("Job-skill records:", len(df))

print("\nTop 30 skills:")
print(df["skills"].value_counts().head(30).to_string())

print(f"\nSaved to: {OUTPUT_FILE}")