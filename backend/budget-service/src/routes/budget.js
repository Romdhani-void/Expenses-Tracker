const express = require('express');
const router = express.Router();
const db = require('../config/database');

// Get all budgets for authenticated user
router.get('/', async (req, res) => {
  try {
    const userId = req.user.id;
    
    const result = await db.query(
      `SELECT b.*, 
        (SELECT COUNT(*) FROM budget_categories WHERE budget_id = b.id) as category_count
       FROM budgets b 
       WHERE b.user_id = $1 
       ORDER BY b.month DESC, b.year DESC`,
      [userId]
    );

    res.json({ budgets: result.rows });
  } catch (error) {
    console.error('Get budgets error:', error);
    res.status(500).json({ error: 'Failed to fetch budgets' });
  }
});

// Get specific budget by ID
router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.id;

    const result = await db.query(
      'SELECT * FROM budgets WHERE id = $1 AND user_id = $2',
      [id, userId]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Budget not found' });
    }

    // Get categories for this budget
    const categories = await db.query(
      'SELECT * FROM budget_categories WHERE budget_id = $1 ORDER BY name',
      [id]
    );

    res.json({
      budget: {
        ...result.rows[0],
        categories: categories.rows,
      },
    });
  } catch (error) {
    console.error('Get budget error:', error);
    res.status(500).json({ error: 'Failed to fetch budget' });
  }
});

// Get budget for specific month/year
router.get('/month/:year/:month', async (req, res) => {
  try {
    const { year, month } = req.params;
    const userId = req.user.id;

    const result = await db.query(
      'SELECT * FROM budgets WHERE user_id = $1 AND year = $2 AND month = $3',
      [userId, year, month]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Budget not found for this month' });
    }

    const budget = result.rows[0];

    // Get categories for this budget
    const categories = await db.query(
      'SELECT * FROM budget_categories WHERE budget_id = $1 ORDER BY name',
      [budget.id]
    );

    res.json({
      budget: {
        ...budget,
        categories: categories.rows,
      },
    });
  } catch (error) {
    console.error('Get budget by month error:', error);
    res.status(500).json({ error: 'Failed to fetch budget' });
  }
});

// Create a new budget
router.post('/', async (req, res) => {
  try {
    const userId = req.user.id;
    const { year, month, currency, opening_balance } = req.body;

    // Validation
    if (!year || !month || !currency) {
      return res.status(400).json({ error: 'Year, month, and currency are required' });
    }

    // Check if budget already exists for this month
    const existing = await db.query(
      'SELECT * FROM budgets WHERE user_id = $1 AND year = $2 AND month = $3',
      [userId, year, month]
    );

    if (existing.rows.length > 0) {
      return res.status(409).json({ error: 'Budget already exists for this month' });
    }

    const result = await db.query(
      `INSERT INTO budgets (user_id, year, month, currency, opening_balance, closing_balance)
       VALUES ($1, $2, $3, $4, $5, $5)
       RETURNING *`,
      [userId, year, month, currency, opening_balance || 0]
    );

    res.status(201).json({
      message: 'Budget created successfully',
      budget: result.rows[0],
    });
  } catch (error) {
    console.error('Create budget error:', error);
    res.status(500).json({ error: 'Failed to create budget' });
  }
});

// Update budget
router.put('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.id;
    const { opening_balance, closing_balance, currency } = req.body;

    // Verify ownership
    const existing = await db.query(
      'SELECT * FROM budgets WHERE id = $1 AND user_id = $2',
      [id, userId]
    );

    if (existing.rows.length === 0) {
      return res.status(404).json({ error: 'Budget not found' });
    }

    const result = await db.query(
      `UPDATE budgets 
       SET opening_balance = COALESCE($1, opening_balance),
           closing_balance = COALESCE($2, closing_balance),
           currency = COALESCE($3, currency),
           updated_at = NOW()
       WHERE id = $4 AND user_id = $5
       RETURNING *`,
      [opening_balance, closing_balance, currency, id, userId]
    );

    res.json({
      message: 'Budget updated successfully',
      budget: result.rows[0],
    });
  } catch (error) {
    console.error('Update budget error:', error);
    res.status(500).json({ error: 'Failed to update budget' });
  }
});

// Delete budget
router.delete('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.id;

    const result = await db.query(
      'DELETE FROM budgets WHERE id = $1 AND user_id = $2 RETURNING *',
      [id, userId]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Budget not found' });
    }

    res.json({ message: 'Budget deleted successfully' });
  } catch (error) {
    console.error('Delete budget error:', error);
    res.status(500).json({ error: 'Failed to delete budget' });
  }
});

module.exports = router;
