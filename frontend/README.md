# Expense Tracker Frontend

React-based frontend for the Expense Tracker application.

## Features

- User authentication (email/password + Google OAuth)
- Monthly budget management
- Transaction tracking (income/expenses)
- Budget vs actual comparison
- Monthly trends and analytics
- Multi-currency support
- Responsive design

## Tech Stack

- React 18
- React Router for navigation
- Axios for API calls
- Recharts for visualizations
- Vite for build tooling

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create a `.env` file:

```env
# Optional: use backend gateway (unset in dev uses Vite proxy)
VITE_API_URL=http://localhost:8080/api
```

### 3. Run Development Server

```bash
npm run dev
```

Frontend will run on `http://localhost:3000`

### 4. Build for Production

```bash
npm run build
```

Built files will be in the `dist` directory.

### 5. Expose the frontend (Nginx on port 80)

To serve the built app with Nginx (e.g. for a frontend image or production host), use [frontend/nginx.conf](nginx.conf). It listens on **port 80**, serves static files from the build, and proxies `/api/*` to the backend gateway (8080). Run Nginx with this config and set `root` to your `frontend/dist` (or copy `dist` into the image’s `/usr/share/nginx/html`). Then the frontend is exposed at **port 80**; the backend stays on **8080**.

## Project Structure

```
frontend/
├── src/
│   ├── components/      # Reusable UI components
│   ├── pages/          # Page components (Login, Dashboard, etc.)
│   ├── services/       # API integration
│   ├── context/        # React context (Auth, etc.)
│   ├── utils/          # Helper functions
│   ├── App.jsx         # Main app component
│   └── main.jsx        # Entry point
├── public/             # Static assets
├── index.html          # HTML template
├── vite.config.js      # Vite configuration
└── package.json        # Dependencies
```

## Key Pages

1. **Login/Register** - User authentication
2. **Dashboard** - Monthly overview with summary cards
3. **Transactions** - Add/edit/delete income and expenses
4. **Budget** - Set monthly budgets and categories
5. **Analytics** - Trends and budget vs actual comparison

## API Integration

All API calls go through the API Gateway at port 8080:

- Auth: `/api/auth/*`
- Budgets: `/api/budgets/*`
- Transactions: `/api/transactions/*`
- Analytics: `/api/analytics/*`

## Development

Start all microservices before running the frontend:

1. Auth Service (port 3001)
2. Budget Service (port 3002)
3. Transaction Service (port 3003)
4. Analytics Service (port 3004)
5. API Gateway (port 8080)

Then start frontend on port 3000.

## License

MIT
