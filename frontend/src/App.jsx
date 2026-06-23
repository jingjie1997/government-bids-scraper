import { useState } from 'react'
import BidsTable from './BidsTable'
import './App.css'

const KEYWORDS = ['設備', '機房', '醫院', '儀器']

export default function App() {
  const [loading, setLoading] = useState(false)
  const [bids, setBids] = useState(null)
  const [error, setError] = useState(null)
  const [activeKeywords, setActiveKeywords] = useState(new Set())

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

  function toggleKeyword(keyword) {
    setActiveKeywords(prev => {
      const next = new Set(prev)
      if (next.has(keyword)) {
        next.delete(keyword)
      } else {
        next.add(keyword)
      }
      return next
    })
  }

  const filteredBids =
    bids === null
      ? null
      : activeKeywords.size === 0
        ? bids
        : bids.filter(bid => [...activeKeywords].some(kw => bid.bid_name?.includes(kw)))

  function handleDownload() {
    if (!filteredBids || filteredBids.length === 0) return
    const headers = ['項次', '機關名稱', '標案案號', '標案名稱', '招標方式', '公告日期', '截止投標日期', '預算金額']
    const keys = ['index', 'agency', 'bid_number', 'bid_name', 'procurement_method', 'announcement_date', 'deadline', 'budget']
    const rows = [headers, ...filteredBids.map(bid => keys.map(k => bid[k] ?? ''))]
    const csv = rows.map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(',')).join('\r\n')
    const blob = new Blob(['﻿' + csv], { type: 'text/csv;charset=utf-8;' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'bids.csv'
    a.click()
    URL.revokeObjectURL(url)
  }

  const hasData = filteredBids !== null && filteredBids.length > 0

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

      <div className="filter-buttons">
        {KEYWORDS.map(kw => (
          <button
            key={kw}
            className={`btn-keyword${activeKeywords.has(kw) ? ' active' : ''}`}
            onClick={() => toggleKeyword(kw)}
          >
            {kw}
          </button>
        ))}
      </div>

      {error && <div className="error">{error}</div>}

      {filteredBids !== null && (
        <>
          {filteredBids.length > 0 && (
            <p className="count">
              共 {filteredBids.length} 筆標案
              {activeKeywords.size > 0 && bids && filteredBids.length < bids.length
                ? `（篩選自 ${bids.length} 筆）`
                : ''}
            </p>
          )}
          <BidsTable bids={filteredBids} />
        </>
      )}
    </div>
  )
}
