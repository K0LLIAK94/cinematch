from pydantic import BaseModel, ConfigDict


class MovieOut(BaseModel):
    id: int
    title: str
    overview: str
    release_date: str
    poster_path: str
    popularity: float
    model_config = ConfigDict(from_attributes=True)
