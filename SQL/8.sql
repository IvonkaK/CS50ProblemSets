SELECT people.name
FROM people
JOIN movies
JOIN stars
ON people.id = stars.person_id AND movies.id = stars.movie_id
WHERE movies.title = "Toy Story";
