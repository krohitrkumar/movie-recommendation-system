-- 1. MOVIES TABLE CLEANING
-- Remove extra spaces
UPDATE movies 
SET title = TRIM(movies.title);
UPDATE movies 
SET genres = TRIM(LOWER(movies.genres));
-- Convert separators for readability
UPDATE movies 
SET genres = REPLACE(movies.genres,'|',', ');
ALTER TABLE movies 
ADD COLUMN  IF NOT EXISTS release_year INT;
UPDATE movies
SET release_year =
CAST(
    SUBSTRING(title FROM '\((\d{4})\)$')
AS INT);
-- 2. TAGS TABLE CLEANING
-- 
UPDATE tags 
SET tag = TRIM(LOWER(tag));
UPDATE tags 
SET tag = REPLACE(tag,' ','_');
DELETE FROM tags
WHERE tag = '';
ALTER TABLE tags 
ADD COLUMN  IF NOT EXISTS tag_date TIMESTAMP;
UPDATE tags 
SET tag_date  = TO_TIMESTAMP(timestamp);
-- 3. GENOME_TAGS TABLE CLEANING
-- 
UPDATE genome_tags
SET tag = REPLACE(TRIM(LOWER(tag)),' ','_');


-- 4. RATINGS TABLE TRANSFORMATION
-- 
ALTER TABLE ratings 
ADD COLUMN  IF NOT EXISTS rating_date TIMESTAMP;
UPDATE ratings
SET rating_date = TO_TIMESTAMP(timestamp);

-- =========================================================
-- 5. LINKS TABLE
-- =========================================================

-- links table mostly contains numeric data
-- No major cleaning required


-- =========================================================
-- 6. GENOME_SCORES TABLE
-- =========================================================

-- genome_scores contains numeric relevance scores
-- No major cleaning required


-- =========================================================
-- 7. PERFORMANCE OPTIMIZATION
-- =========================================================
CREATE INDEX IF NOT EXISTS idx_ratings_movieid
ON ratings(movieId);

CREATE INDEX IF NOT EXISTS idx_ratings_userid
ON ratings(userId);

CREATE INDEX IF NOT EXISTS idx_tags_movieid
ON tags(movieId);

CREATE INDEX IF NOT EXISTS idx_genome_scores_movieid
ON genome_scores(movieId);
-- =========================================================
-- POST-PREPROCESSING VALIDATION
-- =========================================================
-- EMPTY TAGS CHECK 
select * FROM tags
WHERE tag = '';
-- Timestamp validation
SELECT * FROM ratings 
WHERE rating_date IS NULL;

UPDATE movies
SET genres = 'unknown'
WHERE genres = '(no_genres_listed)';
