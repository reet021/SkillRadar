CREATE TABLE job_skills (
    id SERIAL PRIMARY KEY,
    category VARCHAR(100),
    skill VARCHAR(100)
);  

-- ==========================================
-- 1. Top 20 Most Demanded Skills
-- ==========================================

SELECT 
    skill,
    COUNT(*) AS job_count
FROM job_skills
GROUP BY skill
ORDER BY job_count DESC
LIMIT 20;


-- ==========================================
-- 2. Skill Demand by Job Category
-- ==========================================

SELECT 
    category,
    skill,
    COUNT(*) AS job_count
FROM job_skills
GROUP BY category, skill
ORDER BY category, job_count DESC;


-- ==========================================
-- 3. Top 5 Skills per Job Category
-- ==========================================

WITH ranked_skills AS (
    SELECT
        category,
        skill,
        COUNT(*) AS job_count,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY COUNT(*) DESC
        ) AS rank
    FROM job_skills
    GROUP BY category, skill
)
SELECT
    category,
    skill,
    job_count,
    rank
FROM ranked_skills
WHERE rank <= 5
ORDER BY category, rank;