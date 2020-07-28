SELECT movies.title, ratings.rating
FROM movies
JOIN ratings
ON ratings.movie_id = movies.id
WHERE movies.year = 2010 AND ratings.rating is not NULL
ORDER BY ratings.rating DESC, movies.title ASC;
