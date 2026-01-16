import { useEffect, useState } from 'react'
import api from '../services/api'

export default function DataTable() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [pagination, setPagination] = useState({ page: 1, pageSize: 10 })

  useEffect(() => {
    fetchData()
  }, [pagination.page])

  const fetchData = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.getData()
      if (Array.isArray(response.data)) {
        setData(response.data)
      } else if (response.data.data && Array.isArray(response.data.data)) {
        setData(response.data.data)
      } else {
        setData([])
      }
    } catch (err) {
      setError(err.response?.data?.message || err.message || 'Failed to load data')
      console.error('Error fetching data:', err)
      setData([])
    } finally {
      setLoading(false)
    }
  }

  const LoadingState = () => (
    <div className="space-y-4">
      {[...Array(5)].map((_, i) => (
        <div key={i} className="h-12 bg-gray-200 rounded animate-pulse"></div>
      ))}
    </div>
  )

  const ErrorState = () => (
    <div className="p-6 bg-red-50 border border-red-200 rounded-lg">
      <p className="text-red-800 mb-4">{error}</p>
      <div className="space-y-2 mb-4">
        <p className="text-sm text-red-700">Debug info:</p>
        <p className="text-xs text-red-600">API Base URL: {import.meta.env.VITE_API_BASE_URL}</p>
        <p className="text-xs text-red-600">Endpoint: GET /api/data</p>
      </div>
      <button
        onClick={fetchData}
        className="btn-primary"
      >
        Try Again
      </button>
    </div>
  )

  const EmptyState = () => (
    <div className="text-center py-12">
      <p className="text-3xl mb-2">📭</p>
      <p className="text-gray-600">No data available</p>
      <p className="text-gray-500 text-sm mt-2">Try connecting to the backend API</p>
    </div>
  )

  const TableView = () => {
    if (data.length === 0) return <EmptyState />

    // Get all keys from first item for column headers
    const columns = data.length > 0 ? Object.keys(data[0]) : []

    return (
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 border-b">
            <tr>
              {columns.map((column) => (
                <th
                  key={column}
                  className="px-6 py-3 text-left text-sm font-semibold text-gray-700"
                >
                  {column}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, idx) => (
              <tr key={idx} className="border-b hover:bg-gray-50 transition-colors">
                {columns.map((column) => (
                  <td
                    key={`${idx}-${column}`}
                    className="px-6 py-4 text-sm text-gray-700"
                  >
                    {typeof row[column] === 'object'
                      ? JSON.stringify(row[column])
                      : String(row[column])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    )
  }

  return (
    <div>
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Data</h1>
          <p className="text-gray-600 mt-2">Fetched from GET /api/data</p>
        </div>
        <button
          onClick={fetchData}
          disabled={loading}
          className="btn-primary disabled:opacity-50"
        >
          {loading ? 'Refreshing...' : 'Refresh'}
        </button>
      </div>

      <div className="card">
        {loading ? (
          <LoadingState />
        ) : error ? (
          <ErrorState />
        ) : (
          <TableView />
        )}
      </div>

      {data.length > 0 && (
        <div className="mt-4 flex justify-between items-center text-sm text-gray-600">
          <p>Showing {data.length} items</p>
        </div>
      )}
    </div>
  )
}
