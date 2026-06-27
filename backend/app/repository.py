from datetime import datetime, timedelta

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Movie


def upsert_movies(db: Session, results: list[dict]) -> list[Movie]:
    """Кэшируем результаты TMDB в локальную БД."""
    movies: list[Movie] = []
    for r in results:
        if not r.get("id") or not r.get("title"):
            continue
        movie = db.get(Movie, r["id"]) or Movie(id=r["id"])
        movie.title = r.get("title", "")
        movie.overview = r.get("overview", "") or ""
        movie.release_date = r.get("release_date", "") or ""
        movie.poster_path = r.get("poster_path", "") or ""
        movie.popularity = r.get("popularity", 0) or 0
        movie.cached_at = datetime.utcnow()
        db.merge(movie)
        movies.append(movie)
    db.commit()
    return movies


def fresh_cached(db: Session, query: str) -> list[Movie]:
    """Свежий кэш по full-text запросу, если есть."""
    ttl = datetime.utcnow() - timedelta(minutes=settings.cache_ttl_minutes)
    sql = text(
        """
        SELECT * FROM movies
        WHERE cached_at > :ttl
          AND to_tsvector('simple', title || ' ' || overview)
              @@ plainto_tsquery('simple', :q)
        ORDER BY ts_rank(
            to_tsvector('simple', title || ' ' || overview),
            plainto_tsquery('simple', :q)
        ) DESC
        LIMIT 20
        """
    )
    rows = db.execute(sql, {"ttl": ttl, "q": query}).mappings().all()
    return [Movie(**dict(row)) for row in rows]


def local_search(db: Session, query: str) -> list[Movie]:
    """Полнотекстовый поиск по всему локальному кэшу."""
    sql = text(
        """
        SELECT *, ts_rank(
            to_tsvector('simple', title || ' ' || overview),
            plainto_tsquery('simple', :q)
        ) AS rank
        FROM movies
        WHERE to_tsvector('simple', title || ' ' || overview)
              @@ plainto_tsquery('simple', :q)
        ORDER BY rank DESC
        LIMIT 50
        """
    )
    rows = db.execute(sql, {"q": query}).mappings().all()
    return [Movie(**{k: v for k, v in row.items() if k != "rank"}) for row in rows]


def ensure_fulltext_index(db: Session) -> None:
    db.execute(
        text(
            """
            CREATE INDEX IF NOT EXISTS movies_fts_idx
            ON movies
            USING GIN (to_tsvector('simple', title || ' ' || overview))
            """
        )
    )
    db.commit()
