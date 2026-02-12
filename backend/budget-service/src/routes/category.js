const express = require('express');
const router = express.Router();
const db = require('../config/database');

// Get all categories for a budget
router.get('/budget/:budgetId', async (req, res) => {
  try {
    const { budgetId } = req.params;
    const userId = req.user.id;

    // Verify budget belongs to user
    const budget = await db.query(
      'SELECT * FROM budgets WHERE id = $1 AND user_id = $2',
      [budgetId, userId]
    );

    if (budget.rows.length === 0) {
      return res.status(404).json({ error: 'Budget not found' });
    }

    const result = await db.query(
      'SELECT * FROM budget_categories WHERE budget_id = $1 ORDER BY name',
      [budgetId]
    );

    res.json({ categories: result.rows });
  } catch (error) {
    console.error('Get categories error:', error);
    res.status(500).json({ error: 'Failed to fetch categories' });
  }
});

// Create a new category
router.post('/', async (req, res) => {
  try {
    const userId = req.user.id;
    const { budget_id, name, planned_amount, currency, is_recurring, recurring_amount } = req.body;

    // Validation
    if (!budget_id || !name || !currency) {
      return res.status(400).json({ error: 'Budget ID, name, and currency are required' });
    }

    // Verify budget belongs to user
    const budget = await db.query(
      'SELECT * FROM budgets WHERE id = $1 AND user_id = $2',
      [budget_id, userId]
    );

    if (budget.rows.length === 0) {
      return res.status(404).json({ error: 'Budget not found' });
    }

    // Check for duplicate category name in same budget
    const existing = await db.query(
      'SELECT * FROM budget_categories WHERE budget_id = $1 AND LOWER(name) = LOWER($2)',
      [budget_id, name]
    );

    if (existing.rows.length > 0) {
      return res.status(409).json({ error: 'Category with this name already exists in this budget' });
    }

    const result = await db.query(
      `INSERT INTO budget_categories 
       (budget_id, name, planned_amount, actual_amount, currency, is_recurring, recurring_amount)
       VALUES ($1, $2, $3, 0, $4, $5, $6)
       RETURNING *`,
      [budget_id, name, planned_amount || 0, currency, is_recurring || false, recurring_amount || null]
    );

    res.status(201).json({
      message: 'Category created successfully',
      category: result.rows[0],
    });
  } catch (error) {
    console.error('Create category error:', error);
    res.status(500).json({ error: 'Failed to create category' });
  }
});

// Update category
router.put('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.id;
    const { name, planned_amount, actual_amount, currency, is_recurring, recurring_amount } = req.body;

    // Verify category belongs to user's budget
    const category = await db.query(
      `SELECT bc.* FROM budget_categories bc
       JOIN budgets b ON bc.budget_id = b.id
       WHERE bc.id = $1 AND b.user_id = $2`,
      [id, userId]
    );

    if (category.rows.length === 0) {
      return res.status(404).json({ error: 'Category not found' });
    }

    const result = await db.query(
      `UPDATE budget_categories 
       SET name = COALESCE($1, name),
           planned_amount = COALESCE($2, planned_amount),
           actual_amount = COALESCE($3, actual_amount),
           currency = COALESCE($4, currency),
           is_recurring = COALESCE($5, is_recurring),
           recurring_amount = COALESCE($6, recurring_amount),
           updated_at = NOW()
       WHERE id = $7
       RETURNING *`,
      [name, planned_amount, actual_amount, currency, is_recurring, recurring_amount, id]
    );

    res.json({
      message: 'Category updated successfully',
      category: result.rows[0],
    });
  } catch (error) {
    console.error('Update category error:', error);
    res.status(500).json({ error: 'Failed to update category' });
  }
});

// Delete category
router.delete('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.id;

    // Verify category belongs to user's budget
    const result = await db.query(
      `DELETE FROM budget_categories bc
       USING budgets b
       WHERE bc.budget_id = b.id
       AND bc.id = $1
       AND b.user_id = $2
       RETURNING bc.*`,
      [id, userId]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Category not found' });
    }

    res.json({ message: 'Category deleted successfully' });
  } catch (error) {
    console.error('Delete category error:', error);
    res.status(500).json({ error: 'Failed to delete category' });
  }
});

// Bulk create categories (useful for recurring categories)
router.post('/bulk', async (req, res) => {
  try {
    const userId = req.user.id;
    const { budget_id, categories } = req.body;

    if (!budget_id || !Array.isArray(categories) || categories.length === 0) {
      return res.status(400).json({ error: 'Budget ID and categories array are required' });
    }

    // Verify budget belongs to user
    const budget = await db.query(
      'SELECT * FROM budgets WHERE id = $1 AND user_id = $2',
      [budget_id, userId]
    );

    if (budget.rows.length === 0) {
      return res.status(404).json({ error: 'Budget not found' });
    }

    const createdCategories = [];

    for (const cat of categories) {
      const result = await db.query(
        `INSERT INTO budget_categories 
         (budget_id, name, planned_amount, actual_amount, currency, is_recurring, recurring_amount)
         VALUES ($1, $2, $3, 0, $4, $5, $6)
         RETURNING *`,
        [
          budget_id,
          cat.name,
          cat.planned_amount || cat.recurring_amount || 0,
          cat.currency,
          cat.is_recurring || false,
          cat.recurring_amount || null
        ]
      );
      createdCategories.push(result.rows[0]);
    }

    res.status(201).json({
      message: `${createdCategories.length} categories created successfully`,
      categories: createdCategories,
    });
  } catch (error) {
    console.error('Bulk create categories error:', error);
    res.status(500).json({ error: 'Failed to create categories' });
  }
});

module.exports = router;
