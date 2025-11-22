from src.services.crud import CrudService
from src.models.movie import Movie

class MovieService(CrudService):    
    def __init__(self, session):
        super().__init__(session, Movie)

    # Additional movie-specific methods can be added here
    def get_movies_by_genre(self, genre: str):
        movies = self.session.select(self.model).where(self.model.genre == genre).all()
        return movies

    def get_movies_by_year(self, year: int):
        movies = self.session.select(self.model).where(self.model.year == year).all()
        return movies
    
    def search_movies_by_title(self, title_substring: str):
        movies = self.session.select(self.model).where(self.model.title.ilike(f"%{title_substring}%")).all()
        return movies