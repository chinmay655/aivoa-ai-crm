import { useEffect, useState } from 'react'
import { searchHcps } from '../api'
import type { HCP } from '../types'

interface Props {
  selectedId: number | null
  onSelect: (hcp: HCP) => void
}

export default function HcpSearch({ selectedId, onSelect }: Props) {
  const [query, setQuery] = useState('')
  const [hcps, setHcps] = useState<HCP[]>([])
  const [isOpen, setIsOpen] = useState(false)
  const selected = hcps.find((hcp) => hcp.id === selectedId)

  useEffect(() => {
    if (selectedId === null) setQuery('')
  }, [selectedId])

  useEffect(() => {
    const timer = window.setTimeout(async () => {
      try {
        const results = await searchHcps(query)
        setHcps(results)
      } catch {
        setHcps([])
      }
    }, 200)
    return () => window.clearTimeout(timer)
  }, [query])

  return (
    <div className="hcp-search">
      <label htmlFor="hcp-search">HCP Name</label>
      <input
        id="hcp-search"
        value={isOpen ? query : selected?.name ?? query}
        placeholder="Search or select HCP..."
        autoComplete="off"
        onFocus={() => {
          setIsOpen(true)
          if (selected) setQuery('')
        }}
        onChange={(event) => {
          setQuery(event.target.value)
          setIsOpen(true)
        }}
      />
      {isOpen && (
        <div className="search-menu">
          {hcps.length === 0 ? (
            <div className="search-empty">No matching HCP found</div>
          ) : (
            hcps.map((hcp) => (
              <button
                type="button"
                key={hcp.id}
                onMouseDown={(event) => event.preventDefault()}
                onClick={() => {
                  onSelect(hcp)
                  setQuery(hcp.name)
                  setIsOpen(false)
                }}
              >
                <strong>{hcp.name}</strong>
                <span>{hcp.specialty} · {hcp.organization}</span>
              </button>
            ))
          )}
        </div>
      )}
    </div>
  )
}
