import { useState } from 'react'
import BidsTable from './BidsTable'
import './App.css'

export default function App() {
  const [loading, setLoading] = useState(false)
  const [bids, setBids] = useState(null)
  const [error, setError] = useState(null)

  async function handleScrape() {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch('/api/scrape', { method: 'POST' })
      if (!res.ok) {
        const body = await res.json().catch(() => ({}))
        throw new Error(body.error || `伺服器錯誤（HTTP ${res.status}）`)
      }
      const data = await res.json()
      setBids(data.data)
    } catch (err) {
      setError(err.message || '連線失敗，請確認後端伺服器已啟動（port 8000）')
    } finally {
      setLoading(false)
    }
  }

  function handleDownload() {
    window.location.href = '/api/download-csv'
  }

  const hasData = bids !== null && bids.length > 0

  return (
    <div className="app">
      <h1>政府標案爬蟲系統</h1>

      <div className="controls">
        <button
          className="btn-scrape"
          onClick={handleScrape}
          disabled={loading}
        >
          {loading ? '爬取中…' : '爬取標案'}
        </button>
        <button
          className="btn-download"
          onClick={handleDownload}
          disabled={!hasData}
        >
          下載 CSV
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {bids !== null && (
        <>
          {hasData && (
            <p className="count">共 {bids.length} 筆標案</p>
          )}
          <BidsTable bids={bids} />
        </>
      )}
    </div>
  )
}
