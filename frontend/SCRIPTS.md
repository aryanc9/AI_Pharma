# NPM Scripts Reference

## Available Commands

```bash
npm run dev          # Start development server at http://localhost:5173
npm run build        # Build for production (output: dist/)
npm run preview      # Preview production build locally
npm run lint         # Run ESLint to check code quality
```

## Common Tasks

### Development
```bash
# Start dev server with hot reload
npm run dev

# Keep running and auto-refresh on file changes
# Open http://localhost:5173 in browser
```

### Building
```bash
# Create optimized production build
npm run build

# Output directory: dist/
# Files are minified and optimized
# Ready to deploy to Firebase, Netlify, etc.
```

### Previewing
```bash
# Build and preview production locally
npm run build
npm run preview

# Helps test production build before deployment
```

### Code Quality
```bash
# Check for linting errors
npm run lint

# This runs ESLint based on .eslintrc.json
```

## Installing New Packages

### Add a dependency
```bash
npm install package-name

# Example:
npm install react-query
```

### Add dev dependency
```bash
npm install --save-dev package-name

# Example:
npm install --save-dev vitest
```

### Update all packages
```bash
npm update
```

### Remove a package
```bash
npm uninstall package-name
```

## Troubleshooting

### Clear cache
```bash
npm cache clean --force
```

### Reinstall dependencies
```bash
rm -rf node_modules package-lock.json
npm install
```

### Force fresh build
```bash
rm -rf dist
npm run build
```

## Environment

- **Node version**: 16+ recommended
- **npm version**: 8+ recommended

Check versions:
```bash
node --version
npm --version
```

## Docker (Optional)

To run in Docker:
```bash
docker build -t ai-pharma-frontend .
docker run -p 5173:5173 ai-pharma-frontend
```
