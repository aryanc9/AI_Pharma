import { Link, useLocation } from 'react-router-dom'

export default function Sidebar() {
  const location = useLocation()

  const isActive = (path) => location.pathname === path

  const menuItems = [
    { path: '/', label: 'Dashboard', icon: '📊' },
    { path: '/chat', label: 'Chat', icon: '💬' },
    { divider: true, label: 'Admin' },
    { path: '/admin/customers', label: 'Customers', icon: '👥' },
    { path: '/admin/medicines', label: 'Medicines', icon: '💊' },
    { path: '/admin/orders', label: 'Orders', icon: '📦' },
    { path: '/admin/traces', label: 'Decision Traces', icon: '📊' }
  ]

  return (
    <aside className="w-64 bg-white shadow-md flex flex-col max-h-screen overflow-y-auto">
      <div className="p-6 border-b">
        <h1 className="text-2xl font-bold text-primary-600">AI Pharma</h1>
        <p className="text-xs text-gray-500 mt-1">Admin Portal</p>
      </div>

      <nav className="flex-1 px-4 py-6 space-y-1">
        {menuItems.map((item, idx) => {
          if (item.divider) {
            return (
              <div key={idx} className="px-4 py-3 mt-2">
                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                  {item.label}
                </p>
              </div>
            )
          }

          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                isActive(item.path)
                  ? 'bg-primary-100 text-primary-700 font-semibold'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <span className="text-lg">{item.icon}</span>
              <span>{item.label}</span>
            </Link>
          )
        })}
      </nav>

      <div className="p-4 border-t">
        <p className="text-xs text-gray-500">v1.0.0</p>
        <p className="text-xs text-gray-400 mt-1">Backend: Ready</p>
      </div>
    </aside>
  )
}
