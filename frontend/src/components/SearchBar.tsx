interface Props {
  value: string
  onChange: (v: string) => void
}

export function SearchBar({ value, onChange }: Props) {
  return (
    <input
      className="search"
      type="text"
      placeholder="Найти фильм…"
      value={value}
      onChange={(e) => onChange(e.target.value)}
    />
  )
}
