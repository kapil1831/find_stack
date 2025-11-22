from fastapi import APIRouter
from fastapi import Depends
from src.dependency.dependencies import SessionDep
from src.services.movie import MovieService
from src.schemas.movie import MovieCreate, MovieUpdate, MovieRead, MovieList
from fastapi import HTTPException
from typing import List

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)

def get_movie_service(session: SessionDep):
    return MovieService(session)

@router.get("/", response_model=List[MovieRead])
async def get_movies(movie_service=Depends(get_movie_service)):
    movies = movie_service.get_all()
    return movies

@router.get("/{movie_id}", response_model=MovieRead)
async def get_movie(movie_id: int, movie_service=Depends(get_movie_service)):
    movie = movie_service.get(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.post("/", response_model=MovieRead | List[MovieRead])
async def create_movie(movie_payload: MovieCreate | List[MovieCreate], movie_service=Depends(get_movie_service)):
    if isinstance(movie_payload, list):
        movies = movie_service.create_bulk(movie_payload)
        return movies
    else:
        movie = movie_service.create(movie_payload.model_dump())

    if not movie:
        raise HTTPException(status_code=400, detail="Movie could not be created")
    return movie

@router.put("/{movie_id}", response_model=MovieRead)
async def update_movie(movie_id: int, movie_payload: MovieUpdate, movie_service=Depends(get_movie_service)):
    try:
        movie = movie_service.update(movie_id, movie_payload.model_dump(exclude_unset=True))
        return movie
    except Exception as e:
        raise HTTPException(status_code=400, detail="Movie not found or could not be updated")


@router.delete("/{movie_id}", response_model=MovieRead)
async def delete_movie(movie_id: int, movie_service=Depends(get_movie_service)):
    try:
        movie = movie_service.delete(movie_id)
        return movie
    except Exception as e:
        raise HTTPException(status_code=400, detail="Movie not found or could not be deleted")

@router.get("/genre/{genre}", response_model=List[MovieRead])
async def get_movies_by_genre(genre: str, movie_service=Depends(get_movie_service)):
    movies = movie_service.get_movies_by_genre(genre)
    return movies

@router.get("/search/{title}", response_model=List[MovieRead])
async def search_movies_by_title(title: str, movie_service=Depends(get_movie_service)):
    movies = movie_service.search_movies_by_title(title)
    return movies

@router.get("/year/{year}", response_model=List[MovieRead])
async def get_movies_by_year(year: int, movie_service=Depends(get_movie_service)):
    movies = movie_service.get_movies_by_year(year)
    return movies

@router.delete("/", response_model=List[MovieRead])
async def delete_all_movies(movie_service=Depends(get_movie_service)):
    movies = movie_service.delete_all()
    return movies