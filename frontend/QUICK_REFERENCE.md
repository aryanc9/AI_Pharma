# Quick Reference Card

## Setup
```bash
npm install                    # Install dependencies
cp .env.local.example .env.local  # Create env file
npm run dev                   # Start dev server (http://localhost:5173)
```

## Project Structure
```
src/
├── components/    Sidebar, TopNav
├── pages/         LoginPage, Dashboard, DataTable
├── layouts/       DashboardLayout
├── services/      api.js (Axios client)
├── App.jsx        Router & auth logic
└── main.jsx       Entry point
```

## Files Reference
| File | Purpose |
|------|---------|
| `src/App.jsx` | Routes & auth flow |
| `src/pages/*.jsx` | Page components |
| `src/components/*.jsx` | UI components |
| `src/services/api.js` | API client |
| `.env.local` | Environment config |
| `tailwind.config.js` | Tailwind theme |
| `vite.config.js` | Vite settings |

## Environment
```env
VITE_API_BASE_URL=http://localhost:8000
```

## Common Commands
```bash
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Check code quality
```

## Adding a Page
1. Create `src/pages/NewPage.jsx`
2. Add route in `src/App.jsx`
3. Add link in `src/components/Sidebar.jsx`

## Adding an API Endpoint
```javascript
// In src/services/api.js
api.newEndpoint = () => apiClient.get('/api/new')

// In component
const { data } = await api.newEndpoint()
```

## Component Template
```jsx
import { useState, useEffect } from 'react'

export default function ComponentName() {
  const [state, setState] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    // Load data
  }, [])

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>
  
  return <div>Content</div>
}
```

## Tailwind Classes
```jsx
// Buttons
<button className="btn-primary">Primary</button>
<button className="btn-secondary">Secondary</button>

// Cards
<div className="card">Content</div>

// Input
<input className="input-base" placeholder="Text" />

// Grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

// Flexbox
<div className="flex items-center justify-between">

// Spacing
<div className="space-y-4">

// Text
<h1 className="text-3xl font-bold">Title</h1>
<p className="text-gray-600">Subtitle</p>

// Colors
<div className="bg-primary-600 text-white">
<div className="bg-gray-100 text-gray-900">
<div className="bg-red-600 text-white">
```

## Responsive Design
```jsx
// Mobile first
<div className="w-full md:w-1/2 lg:w-1/3">

// Column grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">

// Hide on mobile
<div className="hidden md:block">

// Show only on mobile
<div className="md:hidden">
```

## State Management
```javascript
// useState
const [value, setValue] = useState(null)

// useEffect
useEffect(() => {
  // Run on mount
}, [])

// useEffect with deps
useEffect(() => {
  // Run when dep changes
}, [dependency])
```

## API Patterns
```javascript
// GET request
const { data } = await api.getData()

// Error handling
try {
  const { data } = await api.getData()
  setState(data)
} catch (err) {
  setError(err.message)
}

// Loading state
setLoading(true)
try {
  // api call
} finally {
  setLoading(false)
}
```

## Form Pattern
```jsx
const [formData, setFormData] = useState({})
const [errors, setErrors] = useState({})

const handleChange = (e) => {
  const { name, value } = e.target
  setFormData(prev => ({ ...prev, [name]: value }))
}

const handleSubmit = (e) => {
  e.preventDefault()
  // validate & submit
}

return (
  <form onSubmit={handleSubmit}>
    <input
      name="field"
      value={formData.field}
      onChange={handleChange}
      className="input-base"
    />
    {errors.field && <p className="text-red-600">{errors.field}</p>}
    <button type="submit">Submit</button>
  </form>
)
```

## Debugging
```javascript
console.log('Value:', value)
console.error('Error:', error)
console.table(array)
console.time('label')
console.timeEnd('label')
```

## Browser DevTools
- F12 or Cmd+Option+I
- Console tab → JavaScript errors
- Network tab → API requests
- Elements tab → HTML/CSS
- Sources tab → Breakpoints & debugging

## Deployment
```bash
npm run build              # Create dist folder
firebase deploy            # Deploy to Firebase
```

## Troubleshooting
```bash
# Clear cache
npm cache clean --force

# Reinstall
rm -rf node_modules && npm install

# Force rebuild
rm -rf dist && npm run build

# Check port
lsof -i :5173
```

## File Locations
- Components: `src/components/`
- Pages: `src/pages/`
- API: `src/services/api.js`
- Styling: `src/index.css` + `tailwind.config.js`
- Config: `.env.local`, `vite.config.js`
- Main: `src/App.jsx`, `src/main.jsx`

## Important Files to Edit
- Add pages → `src/pages/`
- Add API endpoints → `src/services/api.js`
- Add navigation → `src/components/Sidebar.jsx`
- Configure colors → `tailwind.config.js`
- Set API URL → `.env.local`

## HTTP Status Codes
- `200` OK (success)
- `201` Created
- `400` Bad Request
- `401` Unauthorized
- `404` Not Found
- `500` Server Error

## Routes
- `/` → Dashboard (protected)
- `/login` → Login page
- `/data` → Data table (protected)

## Auth Token
- Stored in: `localStorage`
- Key: `authToken`
- Usage: Automatically added to API headers

## Responsive Breakpoints
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px

## Colors
- Primary: `bg-primary-600`, `text-primary-600`
- Gray: `bg-gray-100`, `text-gray-900`
- Red: `bg-red-600`, `text-red-600`

## Resources
- [React Docs](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Vite Docs](https://vitejs.dev)
- [React Router](https://reactrouter.com)
- [Axios](https://axios-http.com)

---

**Keep this handy for quick lookups!**
