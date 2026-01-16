import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    // Add admin key for admin endpoints
    if (config.url && config.url.includes('/admin')) {
      config.headers['X-ADMIN-KEY'] = 'dev-admin-key'
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login on unauthorized
      localStorage.removeItem('authToken')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const api = {
  // Health check
  health: () => apiClient.get('/health'),

  // Chat endpoints
  chat: (customerId, message) =>
    apiClient.post('/chat', {
      customer_id: customerId,
      message: message
    }),

  // Admin - Customers
  getCustomers: () => apiClient.get('/admin/customers/'),
  getCustomer: (customerId) => apiClient.get(`/admin/customers/${customerId}`),

  // Admin - Medicines
  getMedicines: () => apiClient.get('/admin/medicines/'),
  getMedicine: (medicineId) => apiClient.get(`/admin/medicines/${medicineId}`),

  // Admin - Orders
  getOrders: () => apiClient.get('/admin/orders/'),
  getOrder: (orderId) => apiClient.get(`/admin/orders/${orderId}`),

  // Admin - Decision Traces
  getDecisionTraces: (limit = 50) =>
    apiClient.get('/admin/decision-traces/', { params: { limit } }),
  getDecisionTrace: (traceId) =>
    apiClient.get(`/admin/decision-traces/${traceId}`),

  // Generic request method
  request: (method, url, data = null, config = {}) => {
    if (method === 'GET') {
      return apiClient.get(url, config)
    }
    if (method === 'POST') {
      return apiClient.post(url, data, config)
    }
    if (method === 'PUT') {
      return apiClient.put(url, data, config)
    }
    if (method === 'DELETE') {
      return apiClient.delete(url, config)
    }
    return Promise.reject(new Error(`Unsupported method: ${method}`))
  }
}

export default api
