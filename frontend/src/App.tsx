import { useEffect, useState } from "react"

import { searchMovies } from "./api/client"
import { MovieCard } from "./components/MovieCard"
import { SearchBar } from "./components/SearchBar"
import { useDebounce } from "./hooks/useDebounce"
import type { Movie } from "./types"

export default function App() {
  const [query, setQuery] = useState("")
  const [movies, setMovies] = useState<Movie[]>([])
  const [loading, setLoading] = useState(false)
  const debounced = useDebounce(query)

  useEffect(() => {
    if (!debounced.trim()) {
      setMovies([])
      return
    }
    let active = true
    setLoading(true)
    searchMovies(debounced)
      .then((data) => {
        if (active) setMovies(data)
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => {
      active = false
    }
  }, [debounced])

  return (
    <div className="app">
      <h1>CineMatch</h1>
      <SearchBar value={query} onChange={setQuery} />
      {loading && <p className="hint">Поиск…</p>}
      <div className="grid">
        {movies.map((m) => (
          <MovieCard key={m.id} movie={m} />
        ))}
      </div>
      {!loading && debounced && movies.length === 0 && (
        <p className="hint">Ничего не найдено.</p>
      )}
    </div>
  )
}
