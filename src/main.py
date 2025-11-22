from fastapi import FastAPI
from src.api.movie import router as movie_router
from src.db.session import create_db_and_tables

app = FastAPI()

app.include_router(router=movie_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/health-check")
async def health_check():
    return {"status": "ok"}