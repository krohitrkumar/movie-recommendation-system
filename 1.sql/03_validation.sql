-- =========================================================
-- 03_VALIDATION.SQL
-- Movie Recommendation System - Data Validation
-- =========================================================


-- =========================================================
-- 1. ROW COUNT VALIDATION
-- =========================================================

SELECT 'movies' AS table_name, COUNT(*) AS total_rows FROM movies
UNION ALL
SELECT 'links', COUNT(*) FROM links
UNION ALL
SELECT 'ratings', COUNT(*) FROM ratings
UNION ALL
SELECT 'tags', COUNT(*) FROM tags
UNION ALL
SELECT 'genome_tags', COUNT(*) FROM genome_tags
UNION ALL
SELECT 'genome_scores', COUNT(*) FROM genome_scores;


-- =========================================================
-- 2. NULL VALUE VALIDATION
-- =========================================================

-- links table
-- imdbId or tmdbId contains NULL values
SELECT *
FROM links
WHERE imdbId IS NULL
   OR tmdbId IS NULL;

-- movies table
-- No NULL values found
SELECT *
FROM movies
WHERE title IS NULL
   OR genres IS NULL;

-- ratings table
-- No NULL values found
SELECT *
FROM ratings
WHERE movieId IS NULL
   OR rating IS NULL;

-- tags table
-- No NULL values found
SELECT *
FROM tags
WHERE tag IS NULL;

-- genome_tags table
-- No NULL values found
SELECT *
FROM genome_tags
WHERE tagId IS NULL
   OR tag IS NULL;

-- genome_scores table
-- No NULL values found
SELECT *
FROM genome_scores
WHERE relevance IS NULL;


-- =========================================================
-- 3. DUPLICATE VALIDATION
-- =========================================================

-- movies table
-- No duplicate movieId found
SELECT movieId, COUNT(*)
FROM movies
GROUP BY movieId
HAVING COUNT(*) > 1;

-- Duplicate movie titles exist
-- Same movie names may occur across different years/remakes
SELECT title, COUNT(*)
FROM movies
GROUP BY title
HAVING COUNT(*) > 1;

-- Duplicate title + genres combinations
SELECT title, genres, COUNT(*)
FROM movies
GROUP BY title, genres
HAVING COUNT(*) > 1;

-- ratings table
-- Duplicate movieId is expected because
-- multiple users can rate the same movie
SELECT movieId, COUNT(*)
FROM ratings
GROUP BY movieId
HAVING COUNT(*) > 1;

-- tags table
-- Same movie can have repeated tags from different users
SELECT movieId, tag, COUNT(*)
FROM tags
GROUP BY movieId, tag
HAVING COUNT(*) > 1;

-- links table
-- No duplicate imdbId + tmdbId combinations
SELECT imdbId, tmdbId, COUNT(*)
FROM links
GROUP BY imdbId, tmdbId
HAVING COUNT(*) > 1;

-- genome_tags table
-- No duplicate tags found
SELECT tag, COUNT(*)
FROM genome_tags
GROUP BY tag
HAVING COUNT(*) > 1;

-- genome_scores table
-- Same movieId can have repeated relevance values
SELECT movieId, relevance, COUNT(*)
FROM genome_scores
GROUP BY movieId, relevance
HAVING COUNT(*) > 1;

-- Same tagId can have repeated relevance values
SELECT tagId, relevance, COUNT(*)
FROM genome_scores
GROUP BY tagId, relevance
HAVING COUNT(*) > 1;

-- movieId + tagId combination should be unique
-- No duplicates found
SELECT movieId, tagId, COUNT(*)
FROM genome_scores
GROUP BY movieId, tagId
HAVING COUNT(*) > 1;


-- =========================================================
-- 4. DATA TYPE / RANGE VALIDATION
-- =========================================================

-- Rating should be between 0 and 5
SELECT *
FROM ratings
WHERE rating < 0
   OR rating > 5;

-- Convert Unix timestamp into readable format
SELECT TO_TIMESTAMP(timestamp)
FROM ratings
LIMIT 10;
-- =========================================================
-- 6. REFERENTIAL INTEGRITY VALIDATION
-- =========================================================


-- ratings.movieId should exist in movies table
SELECT r.movieId
FROM ratings r
LEFT JOIN movies m
ON r.movieId = m.movieId
WHERE m.movieId IS NULL;


-- tags.movieId should exist in movies table
SELECT t.movieId
FROM tags t
LEFT JOIN movies m
ON t.movieId = m.movieId
WHERE m.movieId IS NULL;


-- links.movieId should exist in movies table
SELECT l.movieId
FROM links l
LEFT JOIN movies m
ON l.movieId = m.movieId
WHERE m.movieId IS NULL;


-- genome_scores.movieId should exist in movies table
SELECT gs.movieId
FROM genome_scores gs
LEFT JOIN movies m
ON gs.movieId = m.movieId
WHERE m.movieId IS NULL;


-- genome_scores.tagId should exist in genome_tags table
SELECT gs.tagId
FROM genome_scores gs
LEFT JOIN genome_tags gt
ON gs.tagId = gt.tagId
WHERE gt.tagId IS NULL;

-- =========================================================
-- 5. OUTLIER ANALYSIS
-- =========================================================

-- Users with unusually high rating activity
SELECT userId, COUNT(*) AS total_ratings
FROM ratings
GROUP BY userId
ORDER BY total_ratings DESC
LIMIT 100;