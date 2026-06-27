# CineMatch

Поиск и подбор фильмов — пет-проект для резюме.

**Стек:** React + TypeScript + Vite (фронт), FastAPI + httpx + SQLAlchemy (бэк), PostgreSQL (full-text search).

## Что демонстрирует

- Интеграция с внешним API (TMDB) через `httpx` с кэшированием ответов в БД.
- Полнотекстовый поиск PostgreSQL (`tsvector`, `ts_rank`).
- React + TypeScript: поиск с debounce и карточки результатов.

## Структура

```
backend/   FastAPI + httpx (TMDB) + full-text search
frontend/  React + TS + debounce search
```

## Запуск

```bash
docker compose up -d
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # укажите TMDB_API_KEY
uvicorn app.main:app --reload
```

```bash
cd frontend
npm install
npm run dev
```

## API (кратко)

| Метод | Путь | Описание |
| --- | --- | --- |
| GET | `/movies/search?q=` | Поиск по TMDB + кэш |
| GET | `/movies/local?q=` | Локальный full-text поиск |
| GET | `/movies/{id}/similar` | Похожие фильмы |

## Дальнейшее развитие

- [ ] Избранное и оценки
- [ ] Персональные рекомендации
- [ ] Фильтры по жанрам и годам
