import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import Dashboard from './pages/Dashboard'
import ChatPage from './pages/ChatPage'
import CustomersPage from './pages/CustomersPage'
import MedicinesPage from './pages/MedicinesPage'
import OrdersPage from './pages/OrdersPage'
import DecisionTracesPage from './pages/DecisionTracesPage'
import DashboardLayout from './layouts/DashboardLayout'

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Check if user is already logged in (has auth token)
    const token = localStorage.getItem('authToken')
    setIsAuthenticated(!!token)
    setIsLoading(false)
  }, [])

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <Router>
      <Routes>
        <Route
          path="/login"
          element={isAuthenticated ? <Navigate to="/" /> : <LoginPage setIsAuthenticated={setIsAuthenticated} />}
        />
        <Route
          path="/"
          element={isAuthenticated ? <DashboardLayout><Dashboard /></DashboardLayout> : <Navigate to="/login" />}
        />
        <Route
          path="/chat"
          element={isAuthenticated ? <DashboardLayout><ChatPage /></DashboardLayout> : <Navigate to="/login" />}
        />
        <Route
          path="/admin/customers"
          element={isAuthenticated ? <DashboardLayout><CustomersPage /></DashboardLayout> : <Navigate to="/login" />}
        />
        <Route
          path="/admin/medicines"
          element={isAuthenticated ? <DashboardLayout><MedicinesPage /></DashboardLayout> : <Navigate to="/login" />}
        />
        <Route
          path="/admin/orders"
          element={isAuthenticated ? <DashboardLayout><OrdersPage /></DashboardLayout> : <Navigate to="/login" />}
        />
        <Route
          path="/admin/traces"
          element={isAuthenticated ? <DashboardLayout><DecisionTracesPage /></DashboardLayout> : <Navigate to="/login" />}
        />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  )
}
