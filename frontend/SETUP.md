# AI Pharma Frontend - Quick Start Guide

## ⚡ Getting Started (5 minutes)

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure Environment
```bash
cp .env.local.example .env.local
```

Edit `.env.local` and update the API base URL:
```env
VITE_API_BASE_URL=http://localhost:8000
```

### 3. Start Development Server
```bash
npm run dev
```

Open your browser at `http://localhost:5173`

## 🔐 Login

**Demo Mode (UI-level only):**
- Email: any valid email format
- Password: anything

> Note: This is UI-level authentication for demo. No backend authentication is performed.

## 📁 Project Layout

```
frontend/
├── src/
│   ├── components/          # UI components (Sidebar, TopNav)
│   ├── pages/              # Page components (Login, Dashboard, DataTable)
│   ├── layouts/            # Layout wrappers (DashboardLayout)
│   ├── services/           # API client (api.js)
│   ├── App.jsx             # Main router
│   ├── main.jsx            # Entry point
│   └── index.css           # Global styles
├── package.json            # Dependencies
├── vite.config.js          # Vite configuration
├── tailwind.config.js      # Tailwind CSS config
├── firebase.json           # Firebase Hosting config
└── README.md              # Full documentation
```

## 🚀 Key Features

✅ **Authentication UI** - Login page with form validation
✅ **Dashboard Layout** - Sidebar + Top navigation
✅ **Home Dashboard** - Stats cards with loading states
✅ **Data Table** - Fetches from `/api/data` with error handling
✅ **Responsive Design** - Mobile to desktop
✅ **API Integration** - Centralized Axios client
✅ **Error Handling** - User-friendly error messages
✅ **Loading States** - Skeleton screens

## 🔌 API Integration

### Fetching Data

The Data page automatically fetches from `GET /api/data`:

```javascript
// services/api.js
api.getData()  // Returns: Promise<AxiosResponse>
```

**Expected Response:**
```json
[
  { "id": 1, "name": "Item 1", "value": 100 },
  { "id": 2, "name": "Item 2", "value": 200 }
]
```

### Adding New Endpoints

Edit `src/services/api.js`:
```javascript
export const api = {
  getData: () => apiClient.get('/api/data'),
  getOrders: () => apiClient.get('/api/orders'),  // Add new endpoint
  createOrder: (data) => apiClient.post('/api/orders', data)
}
```

## 🎨 Styling

Uses **Tailwind CSS** with custom utilities:

- `.btn-primary` - Primary button
- `.btn-secondary` - Secondary button  
- `.card` - Card container
- `.input-base` - Form input

Example:
```jsx
<button className="btn-primary">Click me</button>
<div className="card">Content here</div>
```

## 📦 Build for Production

```bash
npm run build
```

Output: `dist/` directory (ready for Firebase Hosting)

## 🔧 Environment Variables

| Variable | Default | Use |
|----------|---------|-----|
| `VITE_API_BASE_URL` | `http://localhost:8000` | Backend API URL |

Access in code:
```javascript
import.meta.env.VITE_API_BASE_URL
```

## 🚨 Troubleshooting

### App won't load
- Check backend is running on correct port
- Verify `VITE_API_BASE_URL` is correct
- Check browser console for errors

### Data page shows error
- Backend `/api/data` endpoint not responding?
- Check CORS settings on backend
- Verify API returns valid JSON

### Build fails
```bash
rm -rf node_modules dist
npm install
npm run build
```

## 📋 File Reference

### Pages
- `src/pages/LoginPage.jsx` - Login form (UI-only)
- `src/pages/Dashboard.jsx` - Home with stats cards
- `src/pages/DataTable.jsx` - Fetches and displays table data

### Components
- `src/components/Sidebar.jsx` - Navigation sidebar
- `src/components/TopNav.jsx` - Top navigation bar

### Services
- `src/services/api.js` - Axios client with interceptors

### Config
- `vite.config.js` - Vite settings
- `tailwind.config.js` - Tailwind CSS theme
- `.env.local` - Environment variables (create from `.env.local.example`)

## ✅ Checklist

- [ ] Dependencies installed (`npm install`)
- [ ] Environment file created (`.env.local`)
- [ ] API base URL configured
- [ ] Dev server running (`npm run dev`)
- [ ] Can login with any credentials
- [ ] Dashboard loads with stats cards
- [ ] Data page shows error or data from backend
- [ ] Responsive on mobile (test with dev tools)

## 📚 Resources

- [React Docs](https://react.dev)
- [Vite Docs](https://vitejs.dev)
- [Tailwind CSS Docs](https://tailwindcss.com)
- [React Router Docs](https://reactrouter.com)
- [Axios Docs](https://axios-http.com)

## 🤝 Next Steps

1. Verify backend is running
2. Test the Data page with real API data
3. Add more pages/features as needed
4. Deploy to Firebase Hosting
5. Configure custom domain

For detailed documentation, see [README.md](./README.md)
