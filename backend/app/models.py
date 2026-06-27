from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.database import Base


class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)  # tmdb id
    title = Column(String, nullable=False)
    overview = Column(String, default="")
    release_date = Column(String, default="")
    poster_path = Column(String, default="")
    popularity = Column(Float, default=0)
    cached_at = Column(DateTime, default=datetime.utcnow)
