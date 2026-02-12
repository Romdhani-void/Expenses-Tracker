const express = require('express');
const cors = require('cors');
const budgetRoutes = require('./routes/budget');
const categoryRoutes = require('./routes/category');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3002;

app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Add hardcoded test user to all requests (NO AUTH)
app.use((req, res, next) => {
  req.user = { 
    id: '00000000-0000-0000-0000-000000000001', 
    email: 'test@example.com',
    name: 'Test User'
  };
  next();
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'OK', service: 'Budget Service' });
});

// Routes (NO AUTH REQUIRED)
app.use('/budgets', budgetRoutes);
app.use('/categories', categoryRoutes);

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({ error: 'Internal server error' });
});

app.listen(PORT, () => {
  console.log(`Budget service running on port ${PORT}`);
});

module.exports = app;
