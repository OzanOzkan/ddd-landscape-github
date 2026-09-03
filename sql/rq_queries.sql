SELECT
    g.ID,
    g.Name,
    g.isDDD1,
    g.isDDD2,
    g.isDDD3,
    (CASE WHEN UPPER(g.isDDD1) = 'YES' THEN 1 ELSE 0 END +
     CASE WHEN UPPER(g.isDDD2) = 'YES' THEN 1 ELSE 0 END +
     CASE WHEN UPPER(g.isDDD3) = 'YES' THEN 1 ELSE 0 END) AS yes_votes,
    CASE 
        WHEN (CASE WHEN UPPER(g.isDDD1) = 'YES' THEN 1 ELSE 0 END +
              CASE WHEN UPPER(g.isDDD2) = 'YES' THEN 1 ELSE 0 END +
              CASE WHEN UPPER(g.isDDD3) = 'YES' THEN 1 ELSE 0 END) >= 2 
        THEN 'YES' 
        ELSE 'NO' 
    END AS LLM_majority_vote
FROM gpt_classification_runs g
WHERE g.ID IN (
    'R_kgDOHY0PUQ',
    'MDEwOlJlcG9zaXRvcnkyOTIwNDMxODU=',
    'R_kgDOJXOV7Q',
    'MDEwOlJlcG9zaXRvcnkxNTQ1NjIxMQ==',
    'MDEwOlJlcG9zaXRvcnk0MDQzNjEzNjE=',
    'R_kgDOJtspoA',
    'R_kgDOJlBREw',
    'MDEwOlJlcG9zaXRvcnkxNjE3Mjk2MDY=',
    'R_kgDOMXoE-g',
    'MDEwOlJlcG9zaXRvcnkxNjgxNTI3NjM=',
    'R_kgDOHIlY3A',
    'R_kgDOLHKZVw',
    'R_kgDOI0QNqA',
    'R_kgDOPKNA2Q',
    'MDEwOlJlcG9zaXRvcnkyNzI2Nzg2OTY=',
    'R_kgDOGwZPJA',
    'MDEwOlJlcG9zaXRvcnkyNjc1MTczMQ==',
    'R_kgDOGGh14w',
    'MDEwOlJlcG9zaXRvcnkxODA2NDk1Njg=',
    'R_kgDOKjlD4Q',
    'MDEwOlJlcG9zaXRvcnkzNTE3OTQwNjg=',
    'MDEwOlJlcG9zaXRvcnk1MTI2ODY0MA==',
    'MDEwOlJlcG9zaXRvcnkzMTU0OTM4NTk=',
    'R_kgDOJZ3O1g',
    'R_kgDOKjgtUQ',
    'MDEwOlJlcG9zaXRvcnkxMjkzMDY4Njg=',
    'MDEwOlJlcG9zaXRvcnkzNzk1NTcyOA==',
    'MDEwOlJlcG9zaXRvcnk3ODMwODM5Mw==',
    'R_kgDOMqOnNA',
    'R_kgDOH5YfDw',
    'R_kgDOI6kO6w',
    'R_kgDOJBF9rQ',
    'R_kgDOOq0tiA',
    'MDEwOlJlcG9zaXRvcnkxNzI4ODQ3OQ==',
    'MDEwOlJlcG9zaXRvcnkxMzU1MDI4MTk=',
    'R_kgDOOCTg7A',
    'R_kgDOPTQe_A',
    'R_kgDOLuIjrA',
    'R_kgDOLAfP2w',
    'R_kgDOMnkrtw',
    'R_kgDOOb-02Q',
    'MDEwOlJlcG9zaXRvcnkzODMzNzI3MzA=',
    'R_kgDOM0WsbQ',
    'MDEwOlJlcG9zaXRvcnk5OTczNjUyMQ==',
    'MDEwOlJlcG9zaXRvcnkzMzE5NzYwNTE=',
    'MDEwOlJlcG9zaXRvcnkxNjU3MzIzNzg=',
    'R_kgDOIsoqxA',
    'MDEwOlJlcG9zaXRvcnkyMjY5MzMzMjI=',
    'R_kgDOPsE1bw',
    'R_kgDOMq7siw'
)
ORDER BY CASE g.ID
    WHEN 'R_kgDOHY0PUQ'                            THEN 1
    WHEN 'MDEwOlJlcG9zaXRvcnkyOTIwNDMxODU='        THEN 2
    WHEN 'R_kgDOJXOV7Q'                            THEN 3
    WHEN 'MDEwOlJlcG9zaXRvcnkxNTQ1NjIxMQ=='        THEN 4
    WHEN 'MDEwOlJlcG9zaXRvcnk0MDQzNjEzNjE='        THEN 5
    WHEN 'R_kgDOJtspoA'                            THEN 6
    WHEN 'R_kgDOJlBREw'                            THEN 7
    WHEN 'MDEwOlJlcG9zaXRvcnkxNjE3Mjk2MDY='        THEN 8
    WHEN 'R_kgDOMXoE-g'                            THEN 9
    WHEN 'MDEwOlJlcG9zaXRvcnkxNjgxNTI3NjM='        THEN 10
    WHEN 'R_kgDOHIlY3A'                            THEN 11
    WHEN 'R_kgDOLHKZVw'                            THEN 12
    WHEN 'R_kgDOI0QNqA'                            THEN 13
    WHEN 'R_kgDOPKNA2Q'                            THEN 14
    WHEN 'MDEwOlJlcG9zaXRvcnkyNzI2Nzg2OTY='        THEN 15
    WHEN 'R_kgDOGwZPJA'                            THEN 16
    WHEN 'MDEwOlJlcG9zaXRvcnkyNjc1MTczMQ=='        THEN 17
    WHEN 'R_kgDOGGh14w'                            THEN 18
    WHEN 'MDEwOlJlcG9zaXRvcnkxODA2NDk1Njg='        THEN 19
    WHEN 'R_kgDOKjlD4Q'                            THEN 20
    WHEN 'MDEwOlJlcG9zaXRvcnkzNTE3OTQwNjg='        THEN 21
    WHEN 'MDEwOlJlcG9zaXRvcnk1MTI2ODY0MA=='        THEN 22
    WHEN 'MDEwOlJlcG9zaXRvcnkzMTU0OTM4NTk='        THEN 23
    WHEN 'R_kgDOJZ3O1g'                            THEN 24
    WHEN 'R_kgDOKjgtUQ'                            THEN 25
    WHEN 'MDEwOlJlcG9zaXRvcnkxMjkzMDY4Njg='        THEN 26
    WHEN 'MDEwOlJlcG9zaXRvcnkzNzk1NTcyOA=='        THEN 27
    WHEN 'MDEwOlJlcG9zaXRvcnk3ODMwODM5Mw=='        THEN 28
    WHEN 'R_kgDOMqOnNA'                            THEN 29
    WHEN 'R_kgDOH5YfDw'                            THEN 30
    WHEN 'R_kgDOI6kO6w'                            THEN 31
    WHEN 'R_kgDOJBF9rQ'                            THEN 32
    WHEN 'R_kgDOOq0tiA'                            THEN 33
    WHEN 'MDEwOlJlcG9zaXRvcnkxNzI4ODQ3OQ=='        THEN 34
    WHEN 'MDEwOlJlcG9zaXRvcnkxMzU1MDI4MTk='        THEN 35
    WHEN 'R_kgDOOCTg7A'                            THEN 36
    WHEN 'R_kgDOPTQe_A'                            THEN 37
    WHEN 'R_kgDOLuIjrA'                            THEN 38
    WHEN 'R_kgDOLAfP2w'                            THEN 39
    WHEN 'R_kgDOMnkrtw'                            THEN 40
    WHEN 'R_kgDOOb-02Q'                            THEN 41
    WHEN 'MDEwOlJlcG9zaXRvcnkzODMzNzI3MzA='        THEN 42
    WHEN 'R_kgDOM0WsbQ'                            THEN 43
    WHEN 'MDEwOlJlcG9zaXRvcnk5OTczNjUyMQ=='        THEN 44
    WHEN 'MDEwOlJlcG9zaXRvcnkzMzE5NzYwNTE='        THEN 45
    WHEN 'MDEwOlJlcG9zaXRvcnkxNjU3MzIzNzg='        THEN 46
    WHEN 'R_kgDOIsoqxA'                            THEN 47
    WHEN 'MDEwOlJlcG9zaXRvcnkyMjY5MzMzMjI='        THEN 48
    WHEN 'R_kgDOPsE1bw'                            THEN 49
    WHEN 'R_kgDOMq7siw'                            THEN 50
END;

/* PR Merge Median Latency */
SELECT 
    AVG(julianday(merged_at) - julianday(created_at)) AS Avg_Merge_Latency_Days,
    (
        SELECT latency
        FROM (
            SELECT 
                (julianday(merged_at) - julianday(created_at)) AS latency,
                ROW_NUMBER() OVER (ORDER BY (julianday(merged_at) - julianday(created_at))) AS rn,
                COUNT(*) OVER () AS total
            FROM pull_requests
            WHERE repository_id IN (SELECT ID FROM included_repositories_after_gpt)
            AND merged_at IS NOT NULL
        )
        WHERE rn = (total + 1) / 2
    ) AS Median_Merge_Latency_Days
FROM pull_requests
WHERE repository_id IN (SELECT ID FROM included_repositories_after_gpt)
AND merged_at IS NOT NULL;

/* Longetivity metrics */ 
SELECT 
    AVG(Longevity_Days) AS Average_Longevity,
    MIN(Longevity_Days) AS Minimum_Longevity,
    MAX(Longevity_Days) AS Maximum_Longevity,
    (
        SELECT Longevity_Days
        FROM (
            SELECT 
                (julianday(MAX(c.commit_date)) - julianday(r.CreatedAt)) AS Longevity_Days,
                ROW_NUMBER() OVER (ORDER BY (julianday(MAX(c.commit_date)) - julianday(r.CreatedAt))) AS rn,
                COUNT(*) OVER () AS total
            FROM repositories r
            JOIN commits c ON r.ID = c.repository_id
            WHERE r.ID IN (SELECT ID FROM included_repositories_after_gpt)
            GROUP BY r.ID
        )
        WHERE rn = (total + 1) / 2
    ) AS Median_Longevity
FROM (
    SELECT 
        (julianday(MAX(c.commit_date)) - julianday(r.CreatedAt)) AS Longevity_Days
    FROM repositories r
    JOIN commits c ON r.ID = c.repository_id
    WHERE r.ID IN (SELECT ID FROM included_repositories_after_gpt)
    GROUP BY r.ID
);

SELECT 
    r.Name AS Project_Name, 
    r.Language AS Primary_Language, 
    COUNT(DISTINCT c.author_email) AS Collaborators, 
    r.StargazersCount AS Stars,
    dal.Architecture_Label AS Dominant_Architecture,
    COUNT(c.ID) AS Commits
FROM ddd_architectural_landscape dal
JOIN repositories r ON dal.ID = r.ID
JOIN commits c ON dal.ID = c.repository_id
GROUP BY dal.ID
HAVING Collaborators > 2    -- Filter for engineered systems (min 3 contributors)
ORDER BY COUNT(c.ID) DESC   -- Rank by Technical Intensity (Commit Volume)
LIMIT 10;

SELECT 
    r.Name, 
    r.Language, 
    COUNT(DISTINCT c.author_email) AS Collaborators, 
    r.StargazersCount AS Stars,
    dal.Architecture_Label AS Dominant_Architecture,
    COUNT(c.ID) AS commitCount
FROM ddd_architectural_landscape dal
JOIN commits c ON dal.ID = c.repository_id
JOIN repositories r ON dal.ID = r.ID
GROUP BY dal.ID
HAVING COUNT(DISTINCT c.author_email) > 2  -- Matches   min_contributors logic
ORDER BY COUNT(c.ID) DESC                  -- Ranks by commit volume as in   script
LIMIT 10;



SELECT 
    dal.ID, 
    r.Name, 
    COUNT(DISTINCT c.author_email) AS CollaboratorCount, 
    COUNT(c.ID) AS CommitCount
FROM ddd_architectural_landscape dal
JOIN commits c ON dal.ID = c.repository_id
JOIN repositories r ON dal.ID = r.ID
GROUP BY dal.ID
HAVING COUNT(DISTINCT c.author_email) > 2
/* CHANGE: Order by the metric defined in RQ3 */
ORDER BY CollaboratorCount DESC 
LIMIT 10;


/* RQ1: Temporal Evolution */
-- Number of verified DDD projects created per year
SELECT Year, COUNT(*) as Project_Count
FROM repositories
WHERE ID IN (SELECT ID FROM included_repositories_after_gpt)
GROUP BY Year
ORDER BY Year;

-- Aggregate commit activity over time for verified projects
SELECT strftime('%Y', commit_date) as Activity_Year, COUNT(*) as Total_Commits
FROM commits
WHERE repository_id IN (SELECT ID FROM included_repositories_after_gpt)
GROUP BY Activity_Year
ORDER BY Activity_Year;

-- Longetivity and continuity
SELECT 
    AVG(Longevity_Days) AS Average_Longevity,
    MIN(Longevity_Days) AS Minimum_Longevity,
    MAX(Longevity_Days) AS Maximum_Longevity
FROM (
    SELECT 
        r.ID,
        r.CreatedAt,
        MAX(c.commit_date) AS Last_Commit,
        (julianday(MAX(c.commit_date)) - julianday(r.CreatedAt)) AS Longevity_Days
    FROM repositories r
    JOIN commits c ON r.ID = c.repository_id
    WHERE r.ID IN (SELECT ID FROM included_repositories_after_gpt)
    GROUP BY r.ID
) AS Project_Longevity_Stats;

/* RQ2: Architectural Taxonomy */
-- Distribution of high-level architectural patterns
SELECT Architecture_Label, 
       COUNT(*) AS Style_Count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM ddd_architectural_landscape), 2) AS Percentage
FROM ddd_architectural_landscape
GROUP BY Architecture_Label
ORDER BY Style_Count DESC;

/* RQ3: Exemplary Projects */
-- Top 10 most prominent DDD projects by stars and contributors
SELECT 
	dal.ID 
    dal.Name, 
    dal.Architecture_Label,
    COUNT(c.ID) as Total_Commits, -- Measures volume of work
    COUNT(DISTINCT c.author_email) as Distinct_Contributors, -- Measures collaboration
    r.StargazersCount,
    r.Description
FROM ddd_architectural_landscape dal
JOIN commits c ON dal.ID = c.repository_id
JOIN repositories r ON dal.ID = r.ID
GROUP BY dal.ID
HAVING Distinct_Contributors > 2 -- Rule of thumb to identify active development [6]
ORDER BY Total_Commits DESC
LIMIT 10;

/* RQ4: Ownership */
-- Ratio of Individual vs. Organisation-owned projects
SELECT OwnerType, COUNT(*) AS Count, 
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM included_repositories_after_gpt), 2) AS Percentage
FROM repositories
WHERE ID IN (SELECT ID FROM included_repositories_after_gpt)
GROUP BY OwnerType;

/* RQ5: Technological and Business Ecosystems */
-- Technological: Top programming languages in the verified DDD landscape
SELECT Language, COUNT(*) AS Count
FROM repositories
WHERE ID IN (SELECT ID FROM included_repositories_after_gpt)
GROUP BY Language
ORDER BY Count DESC;

-- Business: Identification of domains via keyword search in project descriptions
SELECT 
    CASE 
        WHEN (LOWER(r.Name) LIKE '%machine learning%' OR LOWER(r.Description) LIKE '%machine learning%' OR LOWER(rm.content) LIKE '%machine learning%' OR 
              LOWER(r.Name) LIKE '%artificial intelligence%' OR LOWER(r.Description) LIKE '%artificial intelligence%' OR LOWER(rm.content) LIKE '%artificial intelligence%') 
             THEN 'Machine Learning'
             
        WHEN (LOWER(r.Name) LIKE '%software development%' OR LOWER(r.Description) LIKE '%software development%' OR LOWER(rm.content) LIKE '%software development%' OR 
              LOWER(r.Name) LIKE '%database%' OR LOWER(r.Description) LIKE '%database%' OR LOWER(rm.content) LIKE '%database%' OR 
              LOWER(r.Name) LIKE '%network%' OR LOWER(r.Description) LIKE '%network%' OR LOWER(rm.content) LIKE '%network%') 
             THEN 'Traditional Software'
             
        WHEN (LOWER(r.Name) LIKE '%human resources%' OR LOWER(r.Description) LIKE '%human resources%' OR LOWER(rm.content) LIKE '%human resources%' OR 
              LOWER(r.Name) LIKE '%tender%' OR LOWER(r.Description) LIKE '%tender%' OR LOWER(rm.content) LIKE '%tender%' OR 
              LOWER(r.Name) LIKE '%maintenance%' OR LOWER(r.Description) LIKE '%maintenance%' OR LOWER(rm.content) LIKE '%maintenance%') 
             THEN 'Business Services'
             
        WHEN (LOWER(r.Name) LIKE '%sales%' OR LOWER(r.Description) LIKE '%sales%' OR LOWER(rm.content) LIKE '%sales%' OR 
              LOWER(r.Name) LIKE '%shopping%' OR LOWER(r.Description) LIKE '%shopping%' OR LOWER(rm.content) LIKE '%shopping%' OR 
              LOWER(r.Name) LIKE '%ecommerce%' OR LOWER(r.Description) LIKE '%ecommerce%' OR LOWER(rm.content) LIKE '%ecommerce%') 
             THEN 'Sales'
             
        WHEN (LOWER(r.Name) LIKE '%bank%' OR LOWER(r.Description) LIKE '%bank%' OR LOWER(rm.content) LIKE '%bank%' OR 
              LOWER(r.Name) LIKE '%accounting%' OR LOWER(r.Description) LIKE '%accounting%' OR LOWER(rm.content) LIKE '%accounting%' OR 
              LOWER(r.Name) LIKE '%asset%' OR LOWER(r.Description) LIKE '%asset%' OR LOWER(rm.content) LIKE '%asset%') 
             THEN 'Financial Services'
             
        WHEN (LOWER(r.Name) LIKE '%logistics%' OR LOWER(r.Description) LIKE '%logistics%' OR LOWER(rm.content) LIKE '%logistics%' OR 
              LOWER(r.Name) LIKE '%warehouse%' OR LOWER(r.Description) LIKE '%warehouse%' OR LOWER(rm.content) LIKE '%warehouse%' OR 
              LOWER(r.Name) LIKE '%shipping%' OR LOWER(r.Description) LIKE '%shipping%' OR LOWER(rm.content) LIKE '%shipping%') 
             THEN 'Logistics'
             
        WHEN (LOWER(r.Name) LIKE '%insurance%' OR LOWER(r.Description) LIKE '%insurance%' OR LOWER(rm.content) LIKE '%insurance%' OR 
              LOWER(r.Name) LIKE '%claim%' OR LOWER(r.Description) LIKE '%claim%' OR LOWER(rm.content) LIKE '%claim%') 
             THEN 'Insurance'
             
        WHEN (LOWER(r.Name) LIKE '%health%' OR LOWER(r.Description) LIKE '%health%' OR LOWER(rm.content) LIKE '%health%' OR 
              LOWER(r.Name) LIKE '%medical%' OR LOWER(r.Description) LIKE '%medical%' OR LOWER(rm.content) LIKE '%medical%' OR 
              LOWER(r.Name) LIKE '%clinic%' OR LOWER(r.Description) LIKE '%clinic%' OR LOWER(rm.content) LIKE '%clinic%') 
             THEN 'Healthcare'
             
        WHEN (LOWER(r.Name) LIKE '%education%' OR LOWER(r.Description) LIKE '%education%' OR LOWER(rm.content) LIKE '%education%' OR 
              LOWER(r.Name) LIKE '%school%' OR LOWER(r.Description) LIKE '%school%' OR LOWER(rm.content) LIKE '%school%' OR 
              LOWER(r.Name) LIKE '%university%' OR LOWER(r.Description) LIKE '%university%' OR LOWER(rm.content) LIKE '%university%') 
             THEN 'Education'
             
        WHEN (LOWER(r.Name) LIKE '%agriculture%' OR LOWER(r.Description) LIKE '%agriculture%' OR LOWER(rm.content) LIKE '%agriculture%' OR 
              LOWER(r.Name) LIKE '%farm%' OR LOWER(r.Description) LIKE '%farm%' OR LOWER(rm.content) LIKE '%farm%') 
             THEN 'Agriculture'
             
        WHEN (LOWER(r.Name) LIKE '%vacation%' OR LOWER(r.Description) LIKE '%vacation%' OR LOWER(rm.content) LIKE '%vacation%' OR 
              LOWER(r.Name) LIKE '%trip%' OR LOWER(r.Description) LIKE '%trip%' OR LOWER(rm.content) LIKE '%trip%' OR 
              LOWER(r.Name) LIKE '%restaurant%' OR LOWER(r.Description) LIKE '%restaurant%' OR LOWER(rm.content) LIKE '%restaurant%') 
             THEN 'Leisure & Recreation'
             
        WHEN (LOWER(r.Name) LIKE '%publish%' OR LOWER(r.Description) LIKE '%publish%' OR LOWER(rm.content) LIKE '%publish%' OR 
              LOWER(r.Name) LIKE '%photography%' OR LOWER(r.Description) LIKE '%photography%' OR LOWER(rm.content) LIKE '%photography%' OR 
              LOWER(r.Name) LIKE '%book%' OR LOWER(r.Description) LIKE '%book%' OR LOWER(rm.content) LIKE '%book%') 
             THEN 'Media & Publishing'
             
        WHEN (LOWER(r.Name) LIKE '%emergency%' OR LOWER(r.Description) LIKE '%emergency%' OR LOWER(rm.content) LIKE '%emergency%' OR 
              LOWER(r.Name) LIKE '%visa%' OR LOWER(r.Description) LIKE '%visa%' OR LOWER(rm.content) LIKE '%visa%' OR 
              LOWER(r.Name) LIKE '%firefighting%' OR LOWER(r.Description) LIKE '%firefighting%' OR LOWER(rm.content) LIKE '%firefighting%') 
             THEN 'Government Services'
             
        WHEN (LOWER(r.Name) LIKE '%environment%' OR LOWER(r.Description) LIKE '%environment%' OR LOWER(rm.content) LIKE '%environment%' OR 
              LOWER(r.Name) LIKE '%weather%' OR LOWER(r.Description) LIKE '%weather%' OR LOWER(rm.content) LIKE '%weather%') 
             THEN 'Environment'
             
        WHEN (LOWER(r.Name) LIKE '%factory%' OR LOWER(r.Description) LIKE '%factory%' OR LOWER(rm.content) LIKE '%factory%' OR 
              LOWER(r.Name) LIKE '%manufacturing%' OR LOWER(r.Description) LIKE '%manufacturing%' OR LOWER(rm.content) LIKE '%manufacturing%' OR 
              LOWER(r.Name) LIKE '%production%' OR LOWER(r.Description) LIKE '%production%' OR LOWER(rm.content) LIKE '%production%') 
             THEN 'Manufacturing'
             
        WHEN (LOWER(r.Name) LIKE '%personal%' OR LOWER(r.Description) LIKE '%personal%' OR LOWER(rm.content) LIKE '%personal%' OR 
              LOWER(r.Name) LIKE '%hobby%' OR LOWER(r.Description) LIKE '%hobby%' OR LOWER(rm.content) LIKE '%hobby%') 
             THEN 'Personal activities'
             
        ELSE 'Unknown/Other'
    END AS Business_Domain, 
    COUNT(*) AS Count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM included_repositories_after_gpt), 2) AS Percentage
FROM repositories r
LEFT JOIN readme rm ON r.ID = rm.repository_id
WHERE r.ID IN (SELECT ID FROM included_repositories_after_gpt)
GROUP BY Business_Domain
ORDER BY Count DESC;

/* RQ6: Community Engagement and Sustainability */
-- Popularity: Average community reception metrics
WITH RepoEngagement AS (
    -- Aggregate unique identities across all activity types per repository
    SELECT repository_id, COUNT(DISTINCT user_id) AS custom_contributor_count
    FROM (
        SELECT repository_id, author_email AS user_id FROM commits
        UNION
        SELECT repository_id, AuthorID AS user_id FROM pull_requests
        UNION
        SELECT repository_id, AuthorID AS user_id FROM issues
    )
    GROUP BY repository_id
)
SELECT 
    AVG(r.StargazersCount) AS Avg_Stars, 
    AVG(r.ForksCount) AS Avg_Forks, 
    AVG(re.custom_contributor_count) AS Avg_Contributors
FROM repositories r
LEFT JOIN RepoEngagement re ON r.ID = re.repository_id
WHERE r.ID IN (SELECT ID FROM included_repositories_after_gpt);

-- Maintenance: Average Pull Request merge latency (in days)
SELECT AVG(julianday(merged_at) - julianday(created_at)) AS Avg_Merge_Latency_Days
FROM pull_requests
WHERE repository_id IN (SELECT ID FROM included_repositories_after_gpt)
AND merged_at IS NOT NULL;











/* Yearly Growth */
/* How many DDD repositories were created each year from 2010 to 2024? */

SELECT 
    strftime('%Y', CreatedAt) AS year, 
    COUNT(*) AS repo_count
FROM 
    included_repositories ir 
/*WHERE 
    strftime('%Y', CreatedAt) >= '2010'*/
GROUP BY 
    year
ORDER BY 
    year;
   
/* What is the total number of DDD repositories? */
SELECT 
	COUNT (*)
FROM
	repositories;

	
/* Commit Activity */
/* How many commits were made each year across all DDD repositories? */

SELECT 
    strftime('%Y', commit_date) AS year, 
    COUNT(*) AS commit_count
FROM 
    commits
WHERE 
    strftime('%Y', commit_date) >= '2010'
GROUP BY 
    year
ORDER BY 
    year;
   
/* What are the top 5 most active repositories (by total commit count), and how many commits do they have? */
SELECT 
    r.NameWithOwner AS repository_full_name,
    COUNT(c.ID) AS commit_count
FROM 
    commits c
JOIN 
    repositories r
ON 
    c.repository_id = r.ID
GROUP BY 
    r.ID, r.Name, r.NameWithOwner
ORDER BY 
    commit_count DESC
LIMIT 5;


/* Repository Longevity */
/* What is the median and mean time (in years) between repository creation and the most recent commit for DDD repositories? */
WITH repo_commit_differences AS (
    SELECT 
        r.ID AS repository_id,
        (julianday(MAX(c.commit_date)) - julianday(r.CreatedAt)) / 365.0 AS time_difference_years
    FROM 
        repositories r
    JOIN 
        commits c
    ON 
        r.ID = c.repository_id
    GROUP BY 
        r.ID
),
ordered_differences AS (
    SELECT 
        time_difference_years,
        ROW_NUMBER() OVER (ORDER BY time_difference_years) AS row_num,
        COUNT(*) OVER () AS total_count
    FROM 
        repo_commit_differences
)
SELECT 
    AVG(time_difference_years) AS mean_time_years,
    (
        SELECT 
            time_difference_years
        FROM 
            ordered_differences
        WHERE 
            row_num = (total_count + 1) / 2
        OR 
            row_num = (total_count + 2) / 2
        LIMIT 1
    ) AS median_time_years
FROM 
    repo_commit_differences;
   
/* Longevity per repository */
SELECT 
    r.NameWithOwner AS repository_full_name,
    (julianday(MAX(c.commit_date)) - julianday(r.CreatedAt)) / 365.0 AS longevity_years
FROM 
    repositories r
JOIN 
    commits c
ON 
    r.ID = c.repository_id
WHERE 
	strftime('%Y', r.CreatedAt) >= '2010'
GROUP BY 
    r.ID, r.Name, r.NameWithOwner
ORDER BY 
    longevity_years DESC;

   
 
/* Repository Ownership */
/* Ownership Distribution */
/* How many DDD repositories are user-owned vs. organization-owned? */
SELECT 
    OwnerType,
    COUNT(*) AS repo_count
FROM 
    repositories
WHERE 
    OwnerType IN ('User', 'Organization')
GROUP BY 
    OwnerType;

/* Has this ownership distribution changed over time (e.g., per year)? */
SELECT 
    strftime('%Y', CreatedAt) AS year,
    OwnerType,
    COUNT(*) AS repo_count
FROM 
    repositories
WHERE 
    OwnerType IN ('User', 'Organization') AND
    strftime('%Y', CreatedAt) IS NOT NULL
GROUP BY 
    year, OwnerType
ORDER BY 
    year, OwnerType;
   
/* Top Contributors */
/* Are there specific organizations or users that contribute significantly to DDD repositories? */
SELECT 
    Owner AS owner_name,
    OwnerType,
    COUNT(*) AS repo_count
FROM 
    repositories
GROUP BY 
    Owner, OwnerType
HAVING 
    repo_count > (
        SELECT AVG(repo_count) 
        FROM (
            SELECT 
                COUNT(*) AS repo_count
            FROM 
                repositories
            GROUP BY 
                Owner
        )
    )
ORDER BY 
    repo_count DESC;
   
/* The top 5 organizations (or users) with the most commits? */
SELECT 
    r.Owner AS owner_name,
    r.OwnerType,
    COUNT(c.ID) AS commit_count
FROM 
    commits c
JOIN 
    repositories r
ON 
    c.repository_id = r.ID
GROUP BY 
    r.Owner, r.OwnerType
ORDER BY 
    commit_count DESC
LIMIT 5;


/* Programming Languages */
/* How many repositories use each programming language? */
SELECT 
    Language AS programming_language,
    COUNT(*) AS repo_count
FROM 
    repositories
WHERE 
    Language IS NOT NULL
GROUP BY 
    Language
ORDER BY 
    repo_count DESC;
   
 
/* User Contribution */
/* Total number of contributions (internal and external) */
SELECT 
    SUM(total_contributors) AS total_contributors
FROM (
    SELECT COUNT(DISTINCT author) AS total_contributors FROM commits
    UNION ALL
    SELECT COUNT(DISTINCT AuthorName) FROM pull_requests
    UNION ALL
    SELECT COUNT(DISTINCT AuthorName) FROM issues
);


/* Median, Average, and Maximum Number of Contributors per Repository */
WITH commit_contributors AS (
    SELECT 
        repository_id,
        COUNT(DISTINCT author) AS commit_contributors
    FROM 
        commits
    GROUP BY repository_id
),
pr_contributors AS (
    SELECT 
        repository_id,
        COUNT(DISTINCT AuthorName) AS pr_contributors
    FROM 
        pull_requests
    GROUP BY repository_id
),
issue_contributors AS (
    SELECT 
        repository_id,
        COUNT(DISTINCT AuthorName) AS issue_contributors
    FROM 
        issues
    GROUP BY repository_id
),
total_contributors AS (
    SELECT 
        r.ID AS repository_id,
        COALESCE(cc.commit_contributors, 0) +
        COALESCE(prc.pr_contributors, 0) +
        COALESCE(ic.issue_contributors, 0) AS total_contributors
    FROM 
        repositories r
    LEFT JOIN commit_contributors cc ON r.ID = cc.repository_id
    LEFT JOIN pr_contributors prc ON r.ID = prc.repository_id
    LEFT JOIN issue_contributors ic ON r.ID = ic.repository_id
)
-- Calculate Median, Average, and Maximum
SELECT 
    AVG(total_contributors) AS average_contributors,
    MAX(total_contributors) AS max_contributors,
    (SELECT total_contributors 
     FROM total_contributors 
     ORDER BY total_contributors 
     LIMIT 1 OFFSET (SELECT COUNT(*) / 2 FROM total_contributors)) AS median_contributors
FROM 
    total_contributors;


/*  Distribution of Contributions by Internal vs. External Users */
SELECT 
    'Internal' AS contributor_type,
    COUNT(c.commit_id) AS commit_count
FROM 
    commits c
JOIN repositories r ON c.repository_id = r.ID
UNION ALL
SELECT 
    'External' AS contributor_type,
    COUNT(pr.pr_number) + COUNT(i.issue_number) AS contribution_count
FROM 
    pull_requests pr
JOIN repositories r ON pr.repository_id = r.ID
LEFT JOIN issues i ON r.ID = i.repository_id;

/* Trends in user participation over time */
WITH internal_contributors AS (
    SELECT DISTINCT 
        author AS contributor,
        strftime('%Y', commit_date) AS year
    FROM 
        commits
    WHERE 
        commit_date >= '2010-01-01'
),
external_contributors AS (
    SELECT DISTINCT 
        AuthorName AS contributor,
        strftime('%Y', created_at) AS year
    FROM 
        pull_requests
    WHERE 
        created_at >= '2010-01-01'
    UNION ALL
    SELECT DISTINCT 
        AuthorName AS contributor,
        strftime('%Y', created_at) AS year
    FROM 
        issues
    WHERE 
        created_at >= '2010-01-01'
)
SELECT 
    year,
    'Internal' AS contributor_type,
    COUNT(DISTINCT contributor) AS contributor_count
FROM 
    internal_contributors
GROUP BY 
    year
UNION ALL
SELECT 
    year,
    'External' AS contributor_type,
    COUNT(DISTINCT contributor) AS contributor_count
FROM 
    external_contributors
GROUP BY 
    year;


 /* Yearly breakdown of new contributors */
   WITH first_internal_contributors AS (
    SELECT 
        author AS contributor,
        MIN(strftime('%Y', commit_date)) AS first_year
    FROM 
        commits
    WHERE 
        commit_date >= '2010-01-01'
    GROUP BY 
        author
),
first_external_contributors AS (
    SELECT 
        AuthorName AS contributor,
        MIN(strftime('%Y', created_at)) AS first_year
    FROM 
        pull_requests
    WHERE 
        created_at >= '2010-01-01'
    GROUP BY 
        AuthorName
    UNION ALL
    SELECT 
        AuthorName AS contributor,
        MIN(strftime('%Y', created_at)) AS first_year
    FROM 
        issues
    WHERE 
        created_at >= '2010-01-01'
    GROUP BY 
        AuthorName
)
SELECT 
    first_year AS year,
    'Internal' AS contributor_type,
    COUNT(DISTINCT contributor) AS new_contributors
FROM 
    first_internal_contributors
WHERE 
    first_year >= '2010'
GROUP BY 
    first_year
UNION ALL
SELECT 
    first_year AS year,
    'External' AS contributor_type,
    COUNT(DISTINCT contributor) AS new_contributors
FROM 
    first_external_contributors
WHERE 
    first_year >= '2010'
GROUP BY 
    first_year;

/* Repositories with the highest number of contributors */   
CREATE TEMP TABLE commit_contributors AS
SELECT 
    repository_id,
    COUNT(DISTINCT author) AS commit_contributors
FROM 
    commits
GROUP BY 
    repository_id;
CREATE TEMP TABLE pr_contributors AS
SELECT 
    repository_id,
    COUNT(DISTINCT AuthorName) AS pr_contributors
FROM 
    pull_requests
GROUP BY 
    repository_id;
CREATE TEMP TABLE issue_contributors AS
SELECT 
    repository_id,
    COUNT(DISTINCT AuthorName) AS issue_contributors
FROM 
    issues
GROUP BY 
    repository_id;
   
SELECT 
    r.ID AS repository_id,
    r.NameWithOwner AS repository_name,
    COALESCE(cc.commit_contributors, 0) +
    COALESCE(prc.pr_contributors, 0) +
    COALESCE(ic.issue_contributors, 0) AS total_contributors
FROM 
    repositories r
LEFT JOIN commit_contributors cc ON r.ID = cc.repository_id
LEFT JOIN pr_contributors prc ON r.ID = prc.repository_id
LEFT JOIN issue_contributors ic ON r.ID = ic.repository_id
ORDER BY 
    total_contributors DESC
LIMIT 5;

/* Users who contributed to multiple repositories in the sample */
 WITH internal_contributors AS (
    -- Internal contributors: authors of commits
    SELECT 
        author AS contributor,
        COUNT(DISTINCT repository_id) AS internal_count
    FROM 
        commits
    GROUP BY 
        author
),
external_contributors AS (
    -- External contributors: authors of pull requests or issues
    SELECT 
        AuthorName AS contributor,
        COUNT(DISTINCT repository_id) AS external_count
    FROM 
        pull_requests
    GROUP BY 
        AuthorName
    UNION ALL
    SELECT 
        AuthorName AS contributor,
        COUNT(DISTINCT repository_id) AS external_count
    FROM 
        issues
    GROUP BY 
        AuthorName
),
combined_contributors AS (
    -- Combine internal and external contributions
    SELECT 
        contributor,
        SUM(internal_count) AS internal_count,
        SUM(external_count) AS external_count
    FROM (
        SELECT 
            ic.contributor,
            ic.internal_count,
            0 AS external_count
        FROM 
            internal_contributors ic
        UNION ALL
        SELECT 
            ec.contributor,
            0 AS internal_count,
            ec.external_count
        FROM 
            external_contributors ec
    ) grouped_contributors
    GROUP BY 
        contributor
)
SELECT 
    contributor,
    internal_count,
    external_count
FROM 
    combined_contributors
WHERE 
    (internal_count + external_count) >= 2 -- Only contributors to at least 2 repositories
ORDER BY 
    contributor;

   
   
WITH internal_contributors AS (
    -- Internal contributors: authors of commits
    SELECT 
        author AS contributor,
        COUNT(DISTINCT repository_id) AS internal_count
    FROM 
        commits
    GROUP BY 
        author
),
external_contributors AS (
    -- External contributors: authors of pull requests or issues
    SELECT 
        AuthorName AS contributor,
        COUNT(DISTINCT repository_id) AS external_count
    FROM 
        pull_requests
    GROUP BY 
        AuthorName
    UNION ALL
    SELECT 
        AuthorName AS contributor,
        COUNT(DISTINCT repository_id) AS external_count
    FROM 
        issues
    GROUP BY 
        AuthorName
),
combined_contributors AS (
    -- Combine internal and external contributions
    SELECT 
        ic.contributor,
        COALESCE(ic.internal_count, 0) AS internal_count,
        COALESCE(ec.external_count, 0) AS external_count
    FROM 
        internal_contributors ic
    LEFT JOIN external_contributors ec ON ic.contributor = ec.contributor
    UNION
    SELECT 
        ec.contributor,
        COALESCE(ic.internal_count, 0) AS internal_count,
        COALESCE(ec.external_count, 0) AS external_count
    FROM 
        external_contributors ec
    LEFT JOIN internal_contributors ic ON ec.contributor = ic.contributor
)
SELECT 
    contributor,
    MAX(internal_count) AS internal_count,
    MAX(external_count) AS external_count
FROM 
    combined_contributors
WHERE 
    internal_count > 0 AND external_count > 0 -- Only contributors with both internal and external contributions
GROUP BY 
    contributor
ORDER BY 
    contributor;

