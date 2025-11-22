from pydantic import BaseModel, ConfigDict

class MovieBase(BaseModel):
    title: str
    year: int
    genre: str

class MovieCreate(MovieBase):
    pass

class MovieUpdate(BaseModel):
    title: str | None = None
    year: int | None = None
    genre: str | None = None

class MovieRead(MovieBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class MovieList(BaseModel):
    movies: list[MovieRead]