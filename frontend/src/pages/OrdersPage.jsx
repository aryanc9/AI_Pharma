import { useState, useEffect } from 'react'
import api from '../services/api'

export default function OrdersPage() {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedOrder, setSelectedOrder] = useState(null)

  useEffect(() => {
    fetchOrders()
  }, [])

  const fetchOrders = async () => {
    setLoading(true)
    setError(null)
    try {
      const { data } = await api.getOrders()
      setOrders(Array.isArray(data) ? data : data.data || [])
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to load orders')
    } finally {
      setLoading(false)
    }
  }

  const LoadingState = () => (
    <div className="space-y-4">
      {[...Array(8)].map((_, i) => (
        <div key={i} className="h-12 bg-gray-200 rounded animate-pulse"></div>
      ))}
    </div>
  )

  const ErrorState = () => (
    <div className="p-6 bg-red-50 border border-red-200 rounded-lg">
      <p className="text-red-800 mb-4">{error}</p>
      <button onClick={fetchOrders} className="btn-primary">
        Try Again
      </button>
    </div>
  )

  const EmptyState = () => (
    <div className="text-center py-12 card">
      <p className="text-3xl mb-2">📦</p>
      <p className="text-gray-600">No orders found</p>
    </div>
  )

  const TableView = () => {
    if (orders.length === 0) return <EmptyState />

    const stats = {
      totalOrders: orders.length,
      totalQuantity: orders.reduce((sum, o) => sum + (o.quantity || 0), 0),
      uniqueCustomers: new Set(orders.map(o => o.customer_id)).size,
      uniqueMedicines: new Set(orders.map(o => o.medicine_name)).size
    }

    const sortedOrders = [...orders].sort(
      (a, b) => new Date(b.created_at) - new Date(a.created_at)
    )

    return (
      <>
        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="card text-center">
            <p className="text-3xl font-bold text-primary-600">{stats.totalOrders}</p>
            <p className="text-sm text-gray-600">Total Orders</p>
          </div>
          <div className="card text-center">
            <p className="text-3xl font-bold text-blue-600">{stats.totalQuantity}</p>
            <p className="text-sm text-gray-600">Total Units</p>
          </div>
          <div className="card text-center">
            <p className="text-3xl font-bold text-green-600">{stats.uniqueCustomers}</p>
            <p className="text-sm text-gray-600">Customers</p>
          </div>
          <div className="card text-center">
            <p className="text-3xl font-bold text-orange-600">{stats.uniqueMedicines}</p>
            <p className="text-sm text-gray-600">Medicines</p>
          </div>
        </div>

        {/* Table */}
        <div className="card overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Order ID</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Customer ID</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Medicine</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Quantity</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Date</th>
              </tr>
            </thead>
            <tbody>
              {sortedOrders.map((order, idx) => (
                <tr
                  key={order.id || idx}
                  onClick={() => setSelectedOrder(order)}
                  className="border-b hover:bg-gray-50 transition-colors cursor-pointer"
                >
                  <td className="px-6 py-4 text-sm text-gray-900 font-medium">#{order.id}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{order.customer_id}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{order.medicine_name}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    <span className="inline-block px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs font-medium">
                      {order.quantity} units
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">
                    {order.created_at 
                      ? new Date(order.created_at).toLocaleString()
                      : 'N/A'
                    }
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Details Modal */}
        {selectedOrder && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg shadow-lg max-w-md w-full p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-semibold">Order Details</h2>
                <button
                  onClick={() => setSelectedOrder(null)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  ✕
                </button>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Order ID</label>
                  <p className="text-gray-900 font-medium">#{selectedOrder.id}</p>
                </div>

                <div>
                  <label className="block text-sm text-gray-600 mb-1">Customer ID</label>
                  <p className="text-gray-900">{selectedOrder.customer_id}</p>
                </div>

                <div>
                  <label className="block text-sm text-gray-600 mb-1">Medicine</label>
                  <p className="text-gray-900">{selectedOrder.medicine_name}</p>
                </div>

                <div>
                  <label className="block text-sm text-gray-600 mb-1">Quantity</label>
                  <p className="text-gray-900">{selectedOrder.quantity} units</p>
                </div>

                <div>
                  <label className="block text-sm text-gray-600 mb-1">Order Date</label>
                  <p className="text-gray-900">
                    {selectedOrder.created_at 
                      ? new Date(selectedOrder.created_at).toLocaleString()
                      : 'N/A'
                    }
                  </p>
                </div>
              </div>

              <button
                onClick={() => setSelectedOrder(null)}
                className="w-full btn-secondary mt-6"
              >
                Close
              </button>
            </div>
          </div>
        )}
      </>
    )
  }

  return (
    <div>
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Orders</h1>
          <p className="text-gray-600 mt-2">Historical order records</p>
        </div>
        <button onClick={fetchOrders} disabled={loading} className="btn-primary disabled:opacity-50">
          {loading ? 'Refreshing...' : 'Refresh'}
        </button>
      </div>

      {loading ? <LoadingState /> : error ? <ErrorState /> : <TableView />}
    </div>
  )
}
