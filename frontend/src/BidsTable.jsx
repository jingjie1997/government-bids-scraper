const COLUMNS = [
  { key: 'index', label: '項次' },
  { key: 'agency', label: '機關名稱' },
  { key: 'bid_number', label: '標案案號' },
  { key: 'bid_name', label: '標案名稱' },
  { key: 'procurement_method', label: '招標方式' },
  { key: 'announcement_date', label: '公告日期' },
  { key: 'deadline', label: '截止投標日期' },
  { key: 'budget', label: '預算金額' },
]

export default function BidsTable({ bids }) {
  if (bids.length === 0) {
    return <p className="empty">無符合條件的標案</p>
  }

  return (
    <table>
      <thead>
        <tr>
          {COLUMNS.map((col) => (
            <th key={col.key}>{col.label}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {bids.map((bid, i) => (
          <tr key={bid.bid_number || i}>
            {COLUMNS.map((col) => (
              <td key={col.key}>{bid[col.key]}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  )
}
