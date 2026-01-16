import { useState, useEffect } from 'react'
import api from '../services/api'

export default function DecisionTracesPage() {
  const [traces, setTraces] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedTrace, setSelectedTrace] = useState(null)
  const [limit, setLimit] = useState(50)

  useEffect(() => {
    fetchTraces()
  }, [limit])

  const fetchTraces = async () => {
    setLoading(true)
    setError(null)
    try {
      const { data } = await api.getDecisionTraces(limit)
      setTraces(Array.isArray(data) ? data : data.data || [])
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to load decision traces')
    } finally {
      setLoading(false)
    }
  }

  const LoadingState = () => (
    <div className="space-y-4">
      {[...Array(6)].map((_, i) => (
        <div key={i} className="h-16 bg-gray-200 rounded animate-pulse"></div>
      ))}
    </div>
  )

  const ErrorState = () => (
    <div className="p-6 bg-red-50 border border-red-200 rounded-lg">
      <p className="text-red-800 mb-4">{error}</p>
      <button onClick={fetchTraces} className="btn-primary">
        Try Again
      </button>
    </div>
  )

  const EmptyState = () => (
    <div className="text-center py-12 card">
      <p className="text-3xl mb-2">📊</p>
      <p className="text-gray-600">No decision traces recorded</p>
    </div>
  )

  const formatJson = (obj) => {
    return JSON.stringify(obj, null, 2)
  }

  const TableView = () => {
    if (traces.length === 0) return <EmptyState />

    const sortedTraces = [...traces].sort(
      (a, b) => new Date(b.created_at) - new Date(a.created_at)
    )

    return (
      <>
        {/* Controls */}
        <div className="mb-6 card flex gap-4 items-end">
          <div>
            <label className="block text-sm text-gray-600 mb-2">Limit</label>
            <select
              value={limit}
              onChange={(e) => setLimit(Number(e.target.value))}
              className="input-base"
            >
              <option value={10}>10</option>
              <option value={25}>25</option>
              <option value={50}>50</option>
              <option value={100}>100</option>
            </select>
          </div>
        </div>

        {/* List */}
        <div className="space-y-4">
          {sortedTraces.map((trace, idx) => (
            <div
              key={trace.id || idx}
              onClick={() => setSelectedTrace(trace)}
              className="card cursor-pointer hover:shadow-lg transition-all border-l-4 border-primary-600"
            >
              <div className="flex justify-between items-start">
                <div>
                  <p className="font-semibold text-gray-900">Decision Trace #{trace.id}</p>
                  <p className="text-sm text-gray-500 mt-1">
                    {trace.created_at 
                      ? new Date(trace.created_at).toLocaleString()
                      : 'N/A'
                    }
                  </p>
                </div>
                <button className="text-primary-600 hover:text-primary-700 font-medium text-sm">
                  View Details →
                </button>
              </div>

              {/* Preview of trace data */}
              {trace.trace_data && (
                <div className="mt-3 p-2 bg-gray-50 rounded text-xs text-gray-600 max-h-20 overflow-hidden">
                  <pre className="whitespace-pre-wrap break-words font-mono">
                    {typeof trace.trace_data === 'string' 
                      ? trace.trace_data.substring(0, 200)
                      : JSON.stringify(trace.trace_data).substring(0, 200)
                    }...
                  </pre>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Details Modal */}
        {selectedTrace && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg shadow-lg max-w-2xl w-full max-h-96 overflow-y-auto">
              <div className="sticky top-0 bg-white border-b px-6 py-4 flex justify-between items-center">
                <h2 className="text-xl font-semibold">Decision Trace #{selectedTrace.id}</h2>
                <button
                  onClick={() => setSelectedTrace(null)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  ✕
                </button>
              </div>

              <div className="p-6 space-y-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-600 mb-2">ID</label>
                  <p className="text-gray-900">{selectedTrace.id}</p>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-600 mb-2">Created At</label>
                  <p className="text-gray-900">
                    {selectedTrace.created_at 
                      ? new Date(selectedTrace.created_at).toLocaleString()
                      : 'N/A'
                    }
                  </p>
                </div>

                {selectedTrace.trace_data && (
                  <div>
                    <label className="block text-sm font-semibold text-gray-600 mb-2">Trace Data</label>
                    <div className="bg-gray-50 p-4 rounded border border-gray-200 max-h-48 overflow-y-auto">
                      <pre className="whitespace-pre-wrap break-words font-mono text-xs text-gray-700">
                        {typeof selectedTrace.trace_data === 'string'
                          ? selectedTrace.trace_data
                          : formatJson(selectedTrace.trace_data)
                        }
                      </pre>
                    </div>
                  </div>
                )}

                {/* All fields */}
                {Object.entries(selectedTrace).map(([key, value]) => {
                  if (['id', 'created_at', 'trace_data'].includes(key)) return null
                  return (
                    <div key={key}>
                      <label className="block text-sm font-semibold text-gray-600 mb-1 capitalize">
                        {key.replace(/_/g, ' ')}
                      </label>
                      <p className="text-gray-900 text-sm break-words">
                        {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                      </p>
                    </div>
                  )
                })}
              </div>

              <div className="border-t px-6 py-4">
                <button
                  onClick={() => setSelectedTrace(null)}
                  className="w-full btn-secondary"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}
      </>
    )
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Decision Traces</h1>
        <p className="text-gray-600 mt-2">Agent decision logs for auditing and debugging</p>
      </div>

      {loading ? <LoadingState /> : error ? <ErrorState /> : <TableView />}
    </div>
  )
}
