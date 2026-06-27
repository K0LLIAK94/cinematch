import httpx

from app.config import settings


async def _get(path: str, params: dict) -> dict:
    params = {**params, "api_key": settings.tmdb_api_key}
    async with httpx.AsyncClient(base_url=settings.tmdb_base_url, timeout=10) as client:
        resp = await client.get(path, params=params)
        resp.raise_for_status()
        return resp.json()


async def search_movies(query: str) -> list[dict]:
    data = await _get("/search/movie", {"query": query, "language": "ru-RU"})
    return data.get("results", [])


async def similar_movies(movie_id: int) -> list[dict]:
    data = await _get(f"/movie/{movie_id}/similar", {"language": "ru-RU"})
    return data.get("results", [])
