import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Budgets = () => {
  const [budgets, setBudgets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newBudget, setNewBudget] = useState({ year: new Date().getFullYear(), month: new Date().getMonth() + 1, currency: 'USD', opening_balance: 0 });

  useEffect(() => {
    fetchBudgets();
  }, []);

  const fetchBudgets = async () => {
    try {
      const response = await api.get('/budgets');
      setBudgets(response.data.budgets || []);
    } catch (err) {
      setError('Failed to fetch budgets');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await api.post('/budgets', newBudget);
      fetchBudgets();
    } catch (err) {
      setError('Failed to create budget');
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h2>Monthly Budget</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      
      <div className="card" style={{ marginBottom: '20px' }}>
        <h3>Create New Budget</h3>
        <form onSubmit={handleCreate} style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', alignItems: 'flex-end' }}>
          <div className="form-group">
            <label>Year</label>
            <input type="number" value={newBudget.year} onChange={(e) => setNewBudget({...newBudget, year: parseInt(e.target.value)})} required />
          </div>
          <div className="form-group">
            <label>Month</label>
            <input type="number" min="1" max="12" value={newBudget.month} onChange={(e) => setNewBudget({...newBudget, month: parseInt(e.target.value)})} required />
          </div>
          <div className="form-group">
            <label>Currency</label>
            <input type="text" value={newBudget.currency} onChange={(e) => setNewBudget({...newBudget, currency: e.target.value})} required />
          </div>
          <div className="form-group">
            <label>Opening Balance</label>
            <input type="number" step="0.01" value={newBudget.opening_balance} onChange={(e) => setNewBudget({...newBudget, opening_balance: parseFloat(e.target.value)})} required />
          </div>
          <button type="submit" className="btn btn-primary">Create</button>
        </form>
      </div>

      <div className="grid">
        {budgets.map(budget => (
          <div key={budget.id} className="card">
            <h4>{budget.year}-{budget.month}</h4>
            <p><strong>Currency:</strong> {budget.currency}</p>
            <p><strong>Opening:</strong> {budget.opening_balance}</p>
            <p><strong>Closing:</strong> {budget.closing_balance || 'N/A'}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Budgets;
