SELECT people.name
FROM people
WHERE id IN (SELECT DISTINCT(person_id) FROM directors WHERE directors.movie_id IN (SELECT movie_id FROM ratings WHERE ratings.rating >= 9.0));