import { useNavigate } from 'react-router-dom'

export default function TopNav() {
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('authToken')
    navigate('/login')
  }

  return (
    <header className="bg-white shadow-sm px-6 py-4 flex justify-between items-center">
      <h2 className="text-xl font-semibold text-gray-800">Welcome</h2>
      <button
        onClick={handleLogout}
        className="btn-secondary text-sm"
      >
        Logout
      </button>
    </header>
  )
}
