import { useState, useEffect } from 'react'
import api from '../services/api'

export default function MedicinesPage() {
  const [medicines, setMedicines] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchMedicines()
  }, [])

  const fetchMedicines = async () => {
    setLoading(true)
    setError(null)
    try {
      const { data } = await api.getMedicines()
      setMedicines(Array.isArray(data) ? data : data.data || [])
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to load medicines')
    } finally {
      setLoading(false)
    }
  }

  const LoadingState = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {[...Array(6)].map((_, i) => (
        <div key={i} className="h-40 bg-gray-200 rounded animate-pulse"></div>
      ))}
    </div>
  )

  const ErrorState = () => (
    <div className="p-6 bg-red-50 border border-red-200 rounded-lg">
      <p className="text-red-800 mb-4">{error}</p>
      <button onClick={fetchMedicines} className="btn-primary">
        Try Again
      </button>
    </div>
  )

  const EmptyState = () => (
    <div className="text-center py-12 card">
      <p className="text-3xl mb-2">💊</p>
      <p className="text-gray-600">No medicines in inventory</p>
    </div>
  )

  const MedicineCard = ({ medicine }) => {
    const stockStatus = medicine.stock_quantity === 0 ? 'out' : medicine.stock_quantity < 10 ? 'low' : 'ok'
    const statusColors = {
      out: 'bg-red-100 text-red-700',
      low: 'bg-yellow-100 text-yellow-700',
      ok: 'bg-green-100 text-green-700'
    }
    const statusLabels = {
      out: 'Out of Stock',
      low: 'Low Stock',
      ok: 'In Stock'
    }

    return (
      <div className="card">
        <div className="flex justify-between items-start mb-4">
          <h3 className="text-lg font-semibold text-gray-900">{medicine.name}</h3>
          <span className={`inline-block px-2 py-1 rounded text-xs font-medium ${statusColors[stockStatus]}`}>
            {statusLabels[stockStatus]}
          </span>
        </div>

        <div className="space-y-3">
          <div>
            <label className="block text-sm text-gray-600 mb-1">ID</label>
            <p className="text-gray-900 font-medium">{medicine.id}</p>
          </div>

          <div>
            <label className="block text-sm text-gray-600 mb-1">Stock Quantity</label>
            <div className="flex items-center gap-2">
              <span className="text-2xl font-bold text-gray-900">{medicine.stock_quantity}</span>
              <span className="text-sm text-gray-500">units</span>
            </div>
          </div>

          <div>
            <label className="block text-sm text-gray-600 mb-1">Prescription Required</label>
            <span className={`inline-block px-2 py-1 rounded text-sm font-medium ${
              medicine.prescription_required 
                ? 'bg-orange-100 text-orange-700' 
                : 'bg-blue-100 text-blue-700'
            }`}>
              {medicine.prescription_required ? '⚕️ Yes' : 'OTC'}
            </span>
          </div>

          {medicine.created_at && (
            <div>
              <label className="block text-sm text-gray-600 mb-1">Created</label>
              <p className="text-sm text-gray-500">
                {new Date(medicine.created_at).toLocaleDateString()}
              </p>
            </div>
          )}
        </div>
      </div>
    )
  }

  const TableView = () => {
    if (medicines.length === 0) return <EmptyState />

    const stats = {
      total: medicines.length,
      inStock: medicines.filter(m => m.stock_quantity > 0).length,
      lowStock: medicines.filter(m => m.stock_quantity > 0 && m.stock_quantity < 10).length,
      outOfStock: medicines.filter(m => m.stock_quantity === 0).length,
      prescriptionRequired: medicines.filter(m => m.prescription_required).length,
      otc: medicines.filter(m => !m.prescription_required).length
    }

    return (
      <>
        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
          <div className="card text-center">
            <p className="text-3xl font-bold text-primary-600">{stats.total}</p>
            <p className="text-sm text-gray-600">Total Medicines</p>
          </div>
          <div className="card text-center">
            <p className="text-3xl font-bold text-green-600">{stats.inStock}</p>
            <p className="text-sm text-gray-600">In Stock</p>
          </div>
          <div className="card text-center">
            <p className="text-3xl font-bold text-yellow-600">{stats.lowStock}</p>
            <p className="text-sm text-gray-600">Low Stock</p>
          </div>
          <div className="card text-center">
            <p className="text-3xl font-bold text-red-600">{stats.outOfStock}</p>
            <p className="text-sm text-gray-600">Out of Stock</p>
          </div>
          <div className="card text-center">
            <p className="text-3xl font-bold text-orange-600">{stats.prescriptionRequired}</p>
            <p className="text-sm text-gray-600">Prescription</p>
          </div>
          <div className="card text-center">
            <p className="text-3xl font-bold text-blue-600">{stats.otc}</p>
            <p className="text-sm text-gray-600">OTC</p>
          </div>
        </div>

        {/* Medicines Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {medicines.map(medicine => (
            <MedicineCard key={medicine.id} medicine={medicine} />
          ))}
        </div>
      </>
    )
  }

  return (
    <div>
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Medicines</h1>
          <p className="text-gray-600 mt-2">Current inventory and stock levels</p>
        </div>
        <button onClick={fetchMedicines} disabled={loading} className="btn-primary disabled:opacity-50">
          {loading ? 'Refreshing...' : 'Refresh'}
        </button>
      </div>

      {loading ? <LoadingState /> : error ? <ErrorState /> : <TableView />}
    </div>
  )
}
