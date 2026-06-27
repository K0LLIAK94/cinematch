import axios from "axios"

import type { Movie } from "../types"

const api = axios.create({ baseURL: "/api" })

export async function searchMovies(q: string): Promise<Movie[]> {
  const { data } = await api.get("/movies/search", { params: { q } })
  return data
}
