CREATE TABLE IF NOT EXISTS movies (
    movieId INT PRIMARY KEY,
    title TEXT,
    genres TEXT
);

CREATE TABLE IF NOT EXISTS links (
    movieId INT PRIMARY KEY,
    imdbId INT,
    tmdbId INT,
    FOREIGN KEY (movieId) REFERENCES movies(movieId) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS ratings (
    userId INT,
    movieId INT,
    rating NUMERIC(2,1),
    timestamp BIGINT,
    PRIMARY KEY (userId, movieId),
    FOREIGN KEY (movieId) REFERENCES movies(movieId) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS tags (
    userId INT,
    movieId INT,
    tag TEXT,
    timestamp BIGINT,
    PRIMARY KEY (userId, movieId, tag),
    FOREIGN KEY (movieId) REFERENCES movies(movieId) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS  genome_tags (
    tagId INT PRIMARY KEY,
    tag TEXT
);
CREATE TABLE IF NOT EXISTS  genome_scores (
    movieId INT,
    tagId INT,
    relevance NUMERIC(5,4),
    PRIMARY KEY (movieId, tagId),
    FOREIGN KEY (movieId) REFERENCES movies(movieId) ON DELETE CASCADE,
    FOREIGN KEY (tagId) REFERENCES genome_tags(tagId) ON DELETE CASCADE
);