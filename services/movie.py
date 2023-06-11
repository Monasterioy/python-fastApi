from models.movie import Movie as MovieModel


class MovieService:
    def __init__(self, db) -> None:
        self.db = db

    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result

    def get_movie(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
    def get_movie_by_query(self, category):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result
    
    def create_movie(self, movie):
        new_movie = MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        
    def update_movie(self, id, movie):
        movie_find = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        movie_find.title = movie.title
        movie_find.category = movie.category
        movie_find.overview = movie.overview
        movie_find.year = movie.year
        movie_find.rating = movie.rating
        self.db.commit()
        
    def delete_movie(self, id):
        movie_find = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        self.db.delete(movie_find)
        self.db.commit()
