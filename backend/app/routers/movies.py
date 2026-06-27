from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import repository, tmdb
from app.database import get_db
from app.schemas import MovieOut

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/search", response_model=list[MovieOut])
async def search(q: str = Query(min_length=1), db: Session = Depends(get_db)):
    """Сначала проверяем свежий кэш, иначе идём в TMDB."""
    cached = repository.fresh_cached(db, q)
    if cached:
        return cached
    results = await tmdb.search_movies(q)
    return repository.upsert_movies(db, results)


@router.get("/local", response_model=list[MovieOut])
def local(q: str = Query(min_length=1), db: Session = Depends(get_db)):
    return repository.local_search(db, q)


@router.get("/{movie_id}/similar", response_model=list[MovieOut])
async def similar(movie_id: int, db: Session = Depends(get_db)):
    results = await tmdb.similar_movies(movie_id)
    return repository.upsert_movies(db, results)
