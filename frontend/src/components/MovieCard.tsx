import type { Movie } from "../types"

const IMG_BASE = "https://image.tmdb.org/t/p/w200"

export function MovieCard({ movie }: { movie: Movie }) {
  const year = movie.release_date ? movie.release_date.slice(0, 4) : "—"
  return (
    <article className="movie-card">
      {movie.poster_path ? (
        <img src={IMG_BASE + movie.poster_path} alt={movie.title} />
      ) : (
        <div className="poster-placeholder">Нет постера</div>
      )}
      <div className="movie-body">
        <h3>{movie.title}</h3>
        <span className="year">{year}</span>
        <p>{movie.overview || "Описание отсутствует."}</p>
      </div>
    </article>
  )
}
