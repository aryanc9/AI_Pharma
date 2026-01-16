import { useState, useEffect } from 'react'
import api from '../services/api'

export default function CustomersPage() {
  const [customers, setCustomers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedCustomer, setSelectedCustomer] = useState(null)

  useEffect(() => {
    fetchCustomers()
  }, [])

  const fetchCustomers = async () => {
    setLoading(true)
    setError(null)
    try {
      const { data } = await api.getCustomers()
      setCustomers(Array.isArray(data) ? data : data.data || [])
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to load customers')
    } finally {
      setLoading(false)
    }
  }

  const LoadingState = () => (
    <div className="space-y-4">
      {[...Array(5)].map((_, i) => (
        <div key={i} className="h-16 bg-gray-200 rounded animate-pulse"></div>
      ))}
    </div>
  )

  const ErrorState = () => (
    <div className="p-6 bg-red-50 border border-red-200 rounded-lg">
      <p className="text-red-800 mb-4">{error}</p>
      <button onClick={fetchCustomers} className="btn-primary">
        Try Again
      </button>
    </div>
  )

  const EmptyState = () => (
    <div className="text-center py-12">
      <p className="text-3xl mb-2">👥</p>
      <p className="text-gray-600">No customers found</p>
    </div>
  )

  const TableView = () => {
    if (customers.length === 0) return <EmptyState />

    return (
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Customer List */}
        <div className="lg:col-span-1">
          <div className="card max-h-96 overflow-y-auto">
            <h3 className="font-semibold mb-4">Customers ({customers.length})</h3>
            <div className="space-y-2">
              {customers.map(customer => (
                <button
                  key={customer.id}
                  onClick={() => setSelectedCustomer(customer)}
                  className={`w-full text-left p-3 rounded border transition-all ${
                    selectedCustomer?.id === customer.id
                      ? 'bg-primary-100 border-primary-600'
                      : 'border-gray-200 hover:border-primary-300'
                  }`}
                >
                  <div className="font-medium text-sm">{customer.name || 'Customer'}</div>
                  <div className="text-xs text-gray-500">{customer.email || customer.phone}</div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Customer Details */}
        <div className="lg:col-span-2">
          {selectedCustomer ? (
            <div className="card space-y-4">
              <h3 className="text-xl font-semibold">{selectedCustomer.name || 'Customer'}</h3>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm text-gray-600 mb-1">ID</label>
                  <p className="text-lg font-medium">{selectedCustomer.id}</p>
                </div>
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Status</label>
                  <span className={`inline-block px-2 py-1 rounded text-sm font-medium ${
                    selectedCustomer.is_new_user ? 'bg-blue-100 text-blue-700' : 'bg-green-100 text-green-700'
                  }`}>
                    {selectedCustomer.is_new_user ? 'New Customer' : 'Returning Customer'}
                  </span>
                </div>
              </div>

              <div>
                <label className="block text-sm text-gray-600 mb-1">Email</label>
                <p className="text-gray-900">{selectedCustomer.email || 'N/A'}</p>
              </div>

              <div>
                <label className="block text-sm text-gray-600 mb-1">Phone</label>
                <p className="text-gray-900">{selectedCustomer.phone || 'N/A'}</p>
              </div>

              <div>
                <label className="block text-sm text-gray-600 mb-1">Preferred Language</label>
                <p className="text-gray-900">{selectedCustomer.preferred_language || 'English'}</p>
              </div>

              <div>
                <label className="block text-sm text-gray-600 mb-1">Created At</label>
                <p className="text-gray-900">
                  {selectedCustomer.created_at 
                    ? new Date(selectedCustomer.created_at).toLocaleString()
                    : 'N/A'
                  }
                </p>
              </div>
            </div>
          ) : (
            <div className="card text-center py-12 text-gray-500">
              Select a customer to view details
            </div>
          )}
        </div>
      </div>
    )
  }

  return (
    <div>
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Customers</h1>
          <p className="text-gray-600 mt-2">Manage all registered customers</p>
        </div>
        <button onClick={fetchCustomers} disabled={loading} className="btn-primary disabled:opacity-50">
          {loading ? 'Refreshing...' : 'Refresh'}
        </button>
      </div>

      {loading ? <LoadingState /> : error ? <ErrorState /> : <TableView />}
    </div>
  )
}
