-- =====================================================
-- MOVIELENS SQL ANALYTICS PROJECT
-- =====================================================

-- =====================================================
-- 1. MOVIE ANALYSIS
-- =====================================================

-- Total number of movies in dataset
SELECT COUNT(*) AS total_movies
FROM movies;

-- How many movies were released each year?
SELECT release_year,
       COUNT(*) AS total_movies
FROM movies
GROUP BY release_year
ORDER BY release_year;

-- Which are the oldest and newest movies?
SELECT title,
       release_year
FROM movies
WHERE release_year = (SELECT MIN(release_year) FROM movies)
   OR release_year = (SELECT MAX(release_year) FROM movies)
ORDER BY release_year;

-- Which movies received the highest number of ratings?
SELECT m.title,
       COUNT(r.rating) AS total_ratings
FROM movies m
JOIN ratings r
ON m.movieid = r.movieid
GROUP BY m.title
ORDER BY total_ratings DESC
LIMIT 10;

-- Which movies have the highest average ratings?
-- Threshold: minimum 100 ratings
SELECT m.title,
       ROUND(AVG(r.rating),2) AS avg_rating,
       COUNT(r.rating) AS total_ratings
FROM movies m
JOIN ratings r
ON m.movieid = r.movieid
GROUP BY m.title
HAVING COUNT(r.rating) >= 100
ORDER BY avg_rating DESC
LIMIT 10;

-- Highest average rated movies with minimum 500 ratings
SELECT m.title,
       ROUND(AVG(r.rating),2) AS avg_rating,
       COUNT(r.rating) AS total_ratings
FROM movies m
JOIN ratings r
ON m.movieid = r.movieid
GROUP BY m.title
HAVING COUNT(r.rating) >= 500
ORDER BY avg_rating DESC
LIMIT 10;

-- Which movies have no genres listed?
SELECT title,
       genres
FROM movies
WHERE genres = 'unknown';

-- Which genre combinations are most common?
SELECT genres,
       COUNT(*) AS total_movies
FROM movies
WHERE genres != 'unknown'
GROUP BY genres
ORDER BY total_movies DESC
LIMIT 10;


-- =====================================================
-- 2. RATINGS ANALYSIS
-- =====================================================

-- Total number of ratings
SELECT COUNT(*) AS total_ratings
FROM ratings;

-- Average rating across all movies
SELECT ROUND(AVG(rating),2) AS avg_rating
FROM ratings;

-- What is the distribution of ratings?
SELECT rating,
       COUNT(*) AS total_count
FROM ratings
GROUP BY rating
ORDER BY total_count DESC;

-- What are the minimum and maximum ratings?
SELECT MIN(rating) AS min_rating,
       MAX(rating) AS max_rating
FROM ratings;

-- How many ratings does each movie receive on average?
SELECT ROUND(AVG(rating_count),2) AS avg_ratings_per_movie
FROM (
    SELECT movieid,
           COUNT(*) AS rating_count
    FROM ratings
    GROUP BY movieid
) AS movie_rating_counts;

-- Which movies have very few ratings? (Cold Start Problem)
SELECT m.title,
       COUNT(r.rating) AS total_ratings
FROM movies m
JOIN ratings r
ON m.movieid = r.movieid
GROUP BY m.title
HAVING COUNT(r.rating) < 5
ORDER BY total_ratings ASC;

-- Which movies have extremely high rating counts?
SELECT m.title,
       COUNT(r.rating) AS total_ratings
FROM movies m
JOIN ratings r
ON m.movieid = r.movieid
GROUP BY m.title
HAVING COUNT(r.rating) >= 1000
ORDER BY total_ratings DESC
LIMIT 10;


-- =====================================================
-- 3. USER ANALYSIS
-- =====================================================

-- Total number of users
SELECT COUNT(DISTINCT userid) AS total_users
FROM ratings;

-- Which users are most active?
SELECT userid,
       COUNT(*) AS total_ratings
FROM ratings
GROUP BY userid
ORDER BY total_ratings DESC
LIMIT 10;

-- How many ratings does an average user give?
SELECT ROUND(AVG(rating_count),2) AS avg_ratings_per_user
FROM (
    SELECT userid,
           COUNT(*) AS rating_count
    FROM ratings
    GROUP BY userid
) AS avgRating;

-- Which users give the highest average ratings?
-- Threshold: users with minimum 100 ratings
SELECT userid,
       ROUND(AVG(rating),2) AS avg_rating,
       COUNT(*) AS total_ratings
FROM ratings
GROUP BY userid
HAVING COUNT(*) >= 100
ORDER BY avg_rating DESC
LIMIT 10;

-- Which users give the lowest average ratings?
-- Threshold: users with minimum 100 ratings
SELECT userid,
       ROUND(AVG(rating),2) AS avg_rating,
       COUNT(*) AS total_ratings
FROM ratings
GROUP BY userid
HAVING COUNT(*) >= 100
ORDER BY avg_rating ASC
LIMIT 10;

-- Are there outlier users with extremely high activity?
SELECT userid,
       COUNT(*) AS total_ratings
FROM ratings
GROUP BY userid
HAVING COUNT(*) >= 1000
ORDER BY total_ratings DESC;


-- =====================================================
-- 4. GENRE ANALYSIS
-- =====================================================

-- Which genres are most common?
SELECT genres,
       COUNT(*) AS total_movies
FROM movies
WHERE genres != 'unknown'
GROUP BY genres
ORDER BY total_movies DESC
LIMIT 10;

-- Which genres receive the highest ratings?
-- Threshold: minimum 500 ratings
SELECT m.genres,
       ROUND(AVG(r.rating),2) AS avg_rating,
       COUNT(r.rating) AS total_ratings
FROM movies m
JOIN ratings r
ON m.movieid = r.movieid
WHERE genres != 'unknown'
GROUP BY m.genres
HAVING COUNT(r.rating) >= 500
ORDER BY avg_rating DESC
LIMIT 10;

-- Which genres receive the most user engagement?
SELECT m.genres,
       COUNT(r.rating) AS total_ratings
FROM movies m
JOIN ratings r
ON m.movieid = r.movieid
WHERE genres != 'unknown'
GROUP BY m.genres
ORDER BY total_ratings DESC
LIMIT 10;

-- Which genre combinations occur most frequently?
SELECT genres,
       COUNT(*) AS total_movies
FROM movies
WHERE genres != 'unknown'
GROUP BY genres
ORDER BY total_movies DESC
LIMIT 10;

-- Which genres are least common?
SELECT genres,
       COUNT(*) AS total_movies
FROM movies
WHERE genres != 'unknown'
GROUP BY genres
ORDER BY total_movies ASC
LIMIT 10;


-- =====================================================
-- 5. TIME-BASED ANALYSIS
-- =====================================================

-- How has movie production changed over time?
SELECT release_year,
       COUNT(*) AS total_movies
FROM movies
GROUP BY release_year
ORDER BY release_year;

-- Which years had the highest movie releases?
SELECT release_year,
       COUNT(*) AS total_movies
FROM movies
GROUP BY release_year
ORDER BY total_movies DESC
LIMIT 10;

-- How has user rating activity changed over time?
SELECT EXTRACT(YEAR FROM rating_date) AS rating_year,
       COUNT(*) AS total_ratings
FROM ratings
GROUP BY rating_year
ORDER BY rating_year;

-- Which years received the most ratings?
SELECT EXTRACT(YEAR FROM rating_date) AS rating_year,
       COUNT(*) AS total_ratings
FROM ratings
GROUP BY rating_year
ORDER BY total_ratings DESC
LIMIT 10;

-- How do average ratings vary by release year?
SELECT m.release_year,
       ROUND(AVG(r.rating),2) AS avg_rating
FROM movies m
JOIN ratings r
ON m.movieid = r.movieid
GROUP BY m.release_year
ORDER BY m.release_year;


-- =====================================================
-- 6. TAG ANALYSIS
-- =====================================================

-- What are the most common user tags?
SELECT tag,
       COUNT(*) AS total_usage
FROM tags
GROUP BY tag
ORDER BY total_usage DESC
LIMIT 10;

-- Which movies receive the most tags?
SELECT m.title,
       COUNT(t.tag) AS total_tags
FROM movies m
JOIN tags t
ON m.movieid = t.movieid
GROUP BY m.title
ORDER BY total_tags DESC
LIMIT 10;

-- Which users create the most tags?
SELECT userid,
       COUNT(tag) AS total_tags
FROM tags
GROUP BY userid
ORDER BY total_tags DESC
LIMIT 10;

-- Are tags mostly emotional, genre-based, or descriptive?
SELECT tag,
       COUNT(*) AS total_usage
FROM tags
GROUP BY tag
ORDER BY total_usage DESC
LIMIT 20;


-- =====================================================
-- 7. RECOMMENDATION-SYSTEM ANALYSIS
-- =====================================================

-- Which movies are most popular?
SELECT m.title,
       COUNT(r.rating) AS total_ratings
FROM movies m
JOIN ratings r
ON m.movieid = r.movieid
GROUP BY m.title
HAVING COUNT(r.rating) >= 1000
ORDER BY total_ratings DESC
LIMIT 10;

-- Which movies suffer from low interaction counts?
SELECT m.title,
       COUNT(r.rating) AS total_ratings
FROM movies m
JOIN ratings r
ON m.movieid = r.movieid
GROUP BY m.title
HAVING COUNT(r.rating) < 5
ORDER BY total_ratings ASC;

-- Are ratings concentrated on a small number of movies?
SELECT m.title,
       COUNT(r.rating) AS total_ratings
FROM movies m
JOIN ratings r
ON m.movieid = r.movieid
GROUP BY m.title
ORDER BY total_ratings DESC
LIMIT 20;

-- Which users have enough interaction data for recommendation modeling?
SELECT userid,
       COUNT(rating) AS total_ratings
FROM ratings
GROUP BY userid
HAVING COUNT(rating) >= 100
ORDER BY total_ratings DESC;

-- Is the dataset sparse?
SELECT COUNT(DISTINCT userid) AS total_users,
       COUNT(DISTINCT movieid) AS total_movies,
       COUNT(*) AS total_ratings,
       ROUND(
           100.0 * COUNT(*) /
           (COUNT(DISTINCT userid) * COUNT(DISTINCT movieid)),
           4
       ) AS sparsity_percentage
FROM ratings;
-- =====================================================
-- FINAL INSIGHTS
-- =====================================================

-- 1. The MovieLens dataset contains 83,239 movies
-- and more than 33 million ratings, making it a
-- large-scale recommendation dataset.

-- 2. Movie production increased significantly after 1990
-- and peaked around 2015–2018, showing rapid growth
-- in movie releases over recent decades.

-- 3. The dataset contains very old historical movies,
-- with the oldest movie released in 1874.

-- 4. Drama is the most dominant genre in the dataset,
-- followed by documentary and comedy.

-- 5. Genre combinations such as
-- comedy-drama and drama-romance are highly frequent,
-- indicating strong overlap between emotional genres.

-- 6. Ratings are heavily concentrated between
-- 3.0 and 4.0, with rating 4.0 being the most common.
-- This suggests users generally provide positive ratings.

-- 7. Shawshank Redemption (1994) received the
-- highest number of ratings, making it one of the
-- most popular and widely engaged movies.

-- 8. Highly rated movies with large rating counts
-- include Planet Earth, Band of Brothers,
-- The Godfather, and Parasite.

-- 9. A small number of movies dominate user interactions,
-- while many movies receive very few ratings.
-- This indicates a strong long-tail distribution.

-- 10. Many movies suffer from the cold-start problem,
-- where some movies have fewer than 5 ratings
-- and several movies have only 1 rating.

-- 11. The dataset is highly sparse
-- with sparsity around 0.1228%.
-- Most users interact with only a tiny subset
-- of all available movies.

-- 12. User activity is highly imbalanced.
-- A small number of users contribute extremely
-- large numbers of ratings and tags.

-- 13. Some users consistently provide extremely high
-- or extremely low ratings, indicating different
-- user rating behaviors and preferences.

-- 14. User-generated tags are mostly descriptive,
-- emotional, and thematic.
-- Popular tags include:
-- sci-fi, atmospheric, funny, surreal,
-- thought-provoking, and visually appealing.

-- 15. Movies such as Star Wars, Inception,
-- Pulp Fiction, and The Matrix receive very high
-- tagging activity, showing strong community engagement.

-- 16. Rating activity increased significantly after 1996
-- and remained highly active during 2000–2020.

-- 17. Average movie ratings remain relatively stable
-- across years, mostly ranging between 3.3 and 3.7.

-- 18. The dataset contains significant outliers
-- in both user activity and movie popularity,
-- which should be handled carefully during ML modeling.

-- =====================================================
-- RECOMMENDATION SYSTEM INSIGHTS
-- =====================================================

-- 1. The dataset structure is suitable for
-- collaborative filtering recommendation systems
-- because of large user-movie interaction volume.

-- 2. Sparse interactions indicate that
-- matrix factorization techniques such as
-- SVD or ALS may perform effectively.

-- 3. Cold-start movies with very few ratings
-- may require content-based recommendation methods.

-- 4. Tags and genres provide strong metadata
-- features for content-based filtering.

-- 5. Highly active users may introduce popularity bias
-- and should be normalized during modeling.

-- 6. Popular movies dominate interaction counts,
-- which may bias recommendations toward blockbuster films.

-- 7. Genre and tag information can be transformed
-- into feature vectors for similarity-based recommendations.

-- 8. Timestamp information enables future implementation
-- of time-aware recommendation systems.

-- 9. User rating behavior varies significantly,
-- suggesting that user normalization techniques
-- may improve recommendation quality.

-- 10. Due to high sparsity,
-- dimensionality reduction techniques will likely
-- improve recommendation efficiency and scalability.
