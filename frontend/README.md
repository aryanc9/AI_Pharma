# AI Pharma Frontend

A modern React + Vite + Tailwind CSS frontend for the AI Pharma application.

## Tech Stack

- **React 18** - UI library
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router DOM** - Client-side routing
- **Axios** - HTTP client for API calls

## Project Structure

```
src/
├── components/        # Reusable UI components
│   ├── Sidebar.jsx
│   └── TopNav.jsx
├── pages/            # Page components
│   ├── LoginPage.jsx
│   ├── Dashboard.jsx
│   └── DataTable.jsx
├── layouts/          # Layout components
│   └── DashboardLayout.jsx
├── services/         # API and business logic
│   └── api.js
├── App.jsx           # Main app component with routing
├── main.jsx          # Entry point
└── index.css         # Global styles
```

## Setup & Installation

### Prerequisites

- Node.js 16+
- npm or yarn

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
cp .env.local.example .env.local
```

4. Update `.env.local` with your API base URL:
```
VITE_API_BASE_URL=http://localhost:8000
```

## Development

Start the development server:
```bash
npm run dev
```

The app will open at `http://localhost:5173`

### Default Credentials (Demo)

- Email: any email format
- Password: any password

The login is UI-level only for demo purposes.

## Building for Production

Build the optimized production bundle:
```bash
npm run build
```

Output is in the `dist/` directory, ready for Firebase Hosting or any static host.

## Features

### Authentication
- Login page with form validation
- UI-level authentication (stores mock token)
- Automatic redirect to login for unauthorized access
- Logout functionality

### Dashboard
- Responsive sidebar navigation
- Top navigation with logout
- Stats cards with loading states
- Clean, minimal design

### Data Page
- Fetches data from `GET /api/data`
- Dynamic table rendering
- Loading state with skeleton screens
- Error handling with retry
- Empty state display
- Full error debug info

### API Integration
- Centralized API service (`services/api.js`)
- Axios interceptors for auth headers
- Request/response error handling
- Automatic redirect on 401 errors
- Environment variable based configuration

## API Endpoints

The frontend expects the following endpoints:

- `GET /api/data` - Fetch tabular data
- `GET /api/health` - Health check (optional)

### Expected API Response Format

For `GET /api/data`:
```json
[
  {
    "id": 1,
    "name": "Item 1",
    "value": 100
  },
  {
    "id": 2,
    "name": "Item 2",
    "value": 200
  }
]
```

Or wrapped in data property:
```json
{
  "data": [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"}
  ]
}
```

## Styling

### Global Styles
- Custom Tailwind configuration in `tailwind.config.js`
- Global CSS with utility classes in `index.css`
- Responsive design (desktop-first approach)

### Component Styles
- Tailwind utility classes
- Custom Tailwind components:
  - `.btn-primary` - Primary button
  - `.btn-secondary` - Secondary button
  - `.card` - Card container
  - `.input-base` - Form input

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_BASE_URL` | `http://localhost:8000` | Backend API base URL |

## Responsive Breakpoints

- Mobile: Default
- Tablet: `md` (768px)
- Desktop: `lg` (1024px)
- Large: `xl` (1280px)

## Error Handling

- API errors show user-friendly messages
- Retry functionality on data table
- Debug info displayed on error (API URL, endpoint)
- Console logging for debugging
- Loading states prevent duplicate requests

## Firebase Hosting Deployment

1. Install Firebase CLI:
```bash
npm install -g firebase-tools
```

2. Initialize Firebase:
```bash
firebase init hosting
```

3. Build the project:
```bash
npm run build
```

4. Deploy:
```bash
firebase deploy
```

### Firebase Configuration

Ensure your `firebase.json` serves the SPA correctly:
```json
{
  "hosting": {
    "public": "dist",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  }
}
```

## State Management

Currently uses React hooks (`useState`, `useEffect`) for state management. For larger apps, consider:
- Context API
- Redux
- Zustand

## Future Enhancements

- [ ] Add authentication backend integration
- [ ] Implement state management (Context/Redux)
- [ ] Add form validation library (Zod/Yup)
- [ ] Pagination for data table
- [ ] Filter and sort capabilities
- [ ] Dark mode support
- [ ] Accessibility improvements (a11y)
- [ ] Unit tests
- [ ] E2E tests

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Troubleshooting

### API Connection Issues

1. Verify backend is running on the correct port
2. Check `VITE_API_BASE_URL` in `.env.local`
3. Ensure CORS is configured on backend
4. Check browser console for specific errors

### Build Issues

Clear cache and reinstall:
```bash
rm -rf node_modules dist
npm install
npm run build
```

### Dev Server Issues

Restart the dev server:
```bash
npm run dev
```

## License

Proprietary - AI Pharma
