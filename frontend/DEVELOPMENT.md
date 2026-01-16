# Development Guide

## Adding a New Page

### 1. Create the page component
```bash
# src/pages/NewPage.jsx
export default function NewPage() {
  return <div>New Page Content</div>
}
```

### 2. Add route in App.jsx
```jsx
import NewPage from './pages/NewPage'

// In Routes:
<Route
  path="/newpage"
  element={isAuthenticated ? <DashboardLayout><NewPage /></DashboardLayout> : <Navigate to="/login" />}
/>
```

### 3. Add navigation in Sidebar.jsx
```jsx
<Link
  to="/newpage"
  className={`block px-4 py-3 rounded-lg transition-colors ${
    isActive('/newpage') 
      ? 'bg-primary-100 text-primary-700 font-semibold' 
      : 'text-gray-700 hover:bg-gray-100'
  }`}
>
  📄 New Page
</Link>
```

## Adding a New API Endpoint

### 1. Add method to services/api.js
```javascript
export const api = {
  // ... existing
  getOrders: (params) => apiClient.get('/api/orders', { params }),
  createOrder: (data) => apiClient.post('/api/orders', data),
  updateOrder: (id, data) => apiClient.put(`/api/orders/${id}`, data),
  deleteOrder: (id) => apiClient.delete(`/api/orders/${id}`)
}
```

### 2. Use in component
```jsx
import { useState, useEffect } from 'react'
import api from '../services/api'

export default function OrdersPage() {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchOrders()
  }, [])

  const fetchOrders = async () => {
    try {
      const response = await api.getOrders()
      setOrders(response.data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>
  
  return (
    <div>
      {orders.map(order => (
        <div key={order.id}>{order.name}</div>
      ))}
    </div>
  )
}
```

## Creating a Reusable Component

### 1. Create component file
```jsx
// src/components/Button.jsx
export default function Button({ 
  children, 
  variant = 'primary', 
  size = 'md',
  ...props 
}) {
  const baseClasses = 'rounded-lg transition-colors font-semibold'
  
  const variants = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300',
    danger: 'bg-red-600 text-white hover:bg-red-700'
  }
  
  const sizes = {
    sm: 'px-3 py-1 text-sm',
    md: 'px-4 py-2',
    lg: 'px-6 py-3 text-lg'
  }
  
  return (
    <button 
      className={`${baseClasses} ${variants[variant]} ${sizes[size]}`}
      {...props}
    >
      {children}
    </button>
  )
}
```

### 2. Use component
```jsx
import Button from '../components/Button'

<Button variant="primary" size="lg">Click me</Button>
<Button variant="danger" size="sm">Delete</Button>
```

## Form Handling

### Basic Form with Validation
```jsx
import { useState } from 'react'

export default function ContactForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  })
  const [errors, setErrors] = useState({})

  const validate = () => {
    const newErrors = {}
    if (!formData.name) newErrors.name = 'Name is required'
    if (!formData.email) newErrors.email = 'Email is required'
    if (!formData.message) newErrors.message = 'Message is required'
    return newErrors
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    if (errors[name]) setErrors(prev => ({ ...prev, [name]: '' }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const newErrors = validate()
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }
    
    try {
      // Submit form
      console.log('Submitting:', formData)
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input
        type="text"
        name="name"
        value={formData.name}
        onChange={handleChange}
        className="input-base"
        placeholder="Your name"
      />
      {errors.name && <p className="text-red-600 text-sm">{errors.name}</p>}
      
      <button type="submit" className="btn-primary">Send</button>
    </form>
  )
}
```

## State Management with Context

### Create context
```jsx
// src/context/AuthContext.jsx
import { createContext, useState } from 'react'

export const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)

  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  )
}
```

### Use in App.jsx
```jsx
import { AuthProvider } from './context/AuthContext'

export default function App() {
  return (
    <AuthProvider>
      <Router>
        {/* routes */}
      </Router>
    </AuthProvider>
  )
}
```

### Use in component
```jsx
import { useContext } from 'react'
import { AuthContext } from '../context/AuthContext'

export default function Dashboard() {
  const { user } = useContext(AuthContext)
  
  return <div>Welcome {user?.name}</div>
}
```

## Styling Guidelines

### Use Tailwind Classes
```jsx
<div className="flex items-center justify-between bg-white rounded-lg shadow-md p-6">
  <h2 className="text-xl font-semibold text-gray-900">Title</h2>
  <button className="btn-primary">Action</button>
</div>
```

### Responsive Classes
```jsx
{/* Mobile: 1 col, Tablet: 2 cols, Desktop: 3 cols */}
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* items */}
</div>
```

### Common Patterns
```jsx
// Flexbox center
<div className="flex items-center justify-center">

// Stack items vertically with spacing
<div className="space-y-4">

// Text truncation
<p className="truncate">Long text...</p>

// Hover effect
<button className="hover:bg-gray-100 transition-colors">

// Disabled state
<button disabled className="disabled:opacity-50 disabled:cursor-not-allowed">
```

## Debugging

### Console logging
```javascript
console.log('Value:', value)
console.error('Error:', error)
console.table(dataArray)
```

### React DevTools
- Install "React Developer Tools" browser extension
- Inspect component props, state, hooks

### Network tab
- Open DevTools → Network tab
- Watch API requests/responses
- Check status codes and response data

### Break on error
- DevTools → Sources
- Add breakpoints in code
- Step through execution

## Testing Checklist

- [ ] Form validation works
- [ ] Loading states display
- [ ] Error states show retry button
- [ ] API errors handled gracefully
- [ ] Responsive on mobile (375px, 768px, 1024px)
- [ ] Logout works from any page
- [ ] Can't access protected pages without login
- [ ] Data loads on page refresh
- [ ] No console errors

## Performance Tips

1. **Code splitting** - Use React.lazy for pages
2. **Memoization** - Use useMemo, useCallback for expensive operations
3. **Image optimization** - Use modern formats (WebP)
4. **Lazy loading** - Load data on scroll
5. **Debounce search** - Don't fire API on every keystroke
6. **Bundle size** - Check with `npm run build` and vite plugin

## Deployment

### To Firebase
```bash
npm run build
firebase deploy
```

### To Netlify
```bash
npm run build
# Drag dist folder to Netlify
```

### To Vercel
```bash
npm run build
# Connect to Vercel, auto-deploys on push
```

## Common Issues & Solutions

### Issue: "Cannot find module"
**Solution:** Check import path matches actual file location

### Issue: "Blank page after login"
**Solution:** Check router setup, verify route is correct

### Issue: "API calls not working"
**Solution:** Check VITE_API_BASE_URL, verify backend CORS settings

### Issue: "Styles not applying"
**Solution:** Clear `node_modules` and rebuild, verify Tailwind config

### Issue: "Build fails"
**Solution:** Check for TypeScript errors if using TS, validate JSX syntax
