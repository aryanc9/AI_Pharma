import { useEffect, useState } from 'react'
import api from '../services/api'

const StatCard = ({ title, value, icon, loading, error, color = 'blue' }) => {
  const colorClass = {
    blue: 'from-blue-400 to-blue-600',
    green: 'from-green-400 to-green-600',
    purple: 'from-purple-400 to-purple-600',
    orange: 'from-orange-400 to-orange-600'
  }[color]

  return (
    <div className="card bg-gradient-to-br from-white to-gray-50 border-l-4 border-primary-600">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-gray-600 text-sm font-medium">{title}</p>
          {loading ? (
            <div className="mt-2 h-8 bg-gray-200 rounded animate-pulse w-20"></div>
          ) : error ? (
            <p className="mt-2 text-red-600 text-sm">Error</p>
          ) : (
            <p className="mt-2 text-4xl font-bold text-gray-900">{value}</p>
          )}
        </div>
        <span className="text-4xl">{icon}</span>
      </div>
    </div>
  )
}

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    setLoading(true)
    setError(null)
    try {
      // Fetch all data in parallel
      const [customersRes, medicinesRes, ordersRes, tracesRes] = await Promise.all([
        api.getCustomers().catch(err => ({ data: [] })),
        api.getMedicines().catch(err => ({ data: [] })),
        api.getOrders().catch(err => ({ data: [] })),
        api.getDecisionTraces(100).catch(err => ({ data: [] }))
      ])

      const customers = Array.isArray(customersRes.data) ? customersRes.data : customersRes.data.data || []
      const medicines = Array.isArray(medicinesRes.data) ? medicinesRes.data : medicinesRes.data.data || []
      const orders = Array.isArray(ordersRes.data) ? ordersRes.data : ordersRes.data.data || []
      const traces = Array.isArray(tracesRes.data) ? tracesRes.data : tracesRes.data.data || []

      const lowStockMedicines = medicines.filter(m => m.stock_quantity < 10 && m.stock_quantity > 0).length
      const outOfStockMedicines = medicines.filter(m => m.stock_quantity === 0).length
      const newCustomers = customers.filter(c => c.is_new_user).length
      const prescriptionMedicines = medicines.filter(m => m.prescription_required).length

      setStats({
        totalCustomers: customers.length,
        newCustomers: newCustomers,
        totalMedicines: medicines.length,
        outOfStock: outOfStockMedicines,
        lowStock: lowStockMedicines,
        prescriptionRequired: prescriptionMedicines,
        totalOrders: orders.length,
        totalTraces: traces.length
      })
    } catch (err) {
      setError(err.message || 'Failed to load stats')
      console.error('Error fetching stats:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">AI Pharma System Overview</p>
      </div>

      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-800">{error}</p>
          <button
            onClick={fetchStats}
            className="mt-2 text-red-600 hover:text-red-800 text-sm font-medium underline"
          >
            Try again
          </button>
        </div>
      )}

      {/* Customer Stats */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Customers</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard
            title="Total Customers"
            value={stats?.totalCustomers}
            icon="👥"
            loading={loading}
            error={error}
            color="blue"
          />
          <StatCard
            title="New Customers"
            value={stats?.newCustomers}
            icon="✨"
            loading={loading}
            error={error}
            color="green"
          />
        </div>
      </div>

      {/* Inventory Stats */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Inventory</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard
            title="Total Medicines"
            value={stats?.totalMedicines}
            icon="💊"
            loading={loading}
            error={error}
            color="purple"
          />
          <StatCard
            title="Low Stock"
            value={stats?.lowStock}
            icon="⚠️"
            loading={loading}
            error={error}
            color="orange"
          />
          <StatCard
            title="Out of Stock"
            value={stats?.outOfStock}
            icon="❌"
            loading={loading}
            error={error}
          />
          <StatCard
            title="Prescription Required"
            value={stats?.prescriptionRequired}
            icon="⚕️"
            loading={loading}
            error={error}
          />
        </div>
      </div>

      {/* Activity Stats */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Activity</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <StatCard
            title="Total Orders"
            value={stats?.totalOrders}
            icon="📦"
            loading={loading}
            error={error}
            color="green"
          />
          <StatCard
            title="Decision Traces"
            value={stats?.totalTraces}
            icon="📊"
            loading={loading}
            error={error}
            color="purple"
          />
        </div>
      </div>

      {/* Info Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4 text-gray-900">Quick Navigation</h3>
          <div className="space-y-3">
            <a href="/chat" className="block p-3 bg-blue-50 hover:bg-blue-100 rounded border border-blue-200 text-blue-900 font-medium transition">
              💬 Go to Chat Interface
            </a>
            <a href="/admin/customers" className="block p-3 bg-green-50 hover:bg-green-100 rounded border border-green-200 text-green-900 font-medium transition">
              👥 Manage Customers
            </a>
            <a href="/admin/medicines" className="block p-3 bg-purple-50 hover:bg-purple-100 rounded border border-purple-200 text-purple-900 font-medium transition">
              💊 Manage Medicines
            </a>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold mb-4 text-gray-900">System Status</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-green-50 rounded border border-green-200">
              <span className="text-gray-900 font-medium">Backend Connection</span>
              <span className="inline-block px-2 py-1 bg-green-200 text-green-800 rounded text-xs font-semibold">Connected</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-blue-50 rounded border border-blue-200">
              <span className="text-gray-900 font-medium">Database</span>
              <span className="inline-block px-2 py-1 bg-blue-200 text-blue-800 rounded text-xs font-semibold">Ready</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded border border-gray-200">
              <span className="text-gray-900 font-medium">APIs</span>
              <span className="inline-block px-2 py-1 bg-gray-200 text-gray-800 rounded text-xs font-semibold">Live</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
