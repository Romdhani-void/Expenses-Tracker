import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Transactions = () => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newTransaction, setNewTransaction] = useState({
    type: 'expense',
    amount: 0,
    currency: 'USD',
    category: 'Food',
    date: new Date().toISOString().split('T')[0],
    notes: ''
  });

  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    try {
      const response = await api.get('/transactions');
      setTransactions(response.data.transactions || []);
    } catch (err) {
      setError('Failed to fetch transactions');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await api.post('/transactions', newTransaction);
      fetchTransactions();
    } catch (err) {
      setError('Failed to add transaction');
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h2>Transactions</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <div className="card" style={{ marginBottom: '20px' }}>
        <h3>Add New Transaction</h3>
        <form onSubmit={handleCreate} style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '10px', alignItems: 'flex-end' }}>
          <div className="form-group">
            <label>Type</label>
            <select value={newTransaction.type} onChange={(e) => setNewTransaction({...newTransaction, type: e.target.value})}>
              <option value="income">Income</option>
              <option value="expense">Expense</option>
            </select>
          </div>
          <div className="form-group">
            <label>Amount</label>
            <input type="number" step="0.01" value={newTransaction.amount} onChange={(e) => setNewTransaction({...newTransaction, amount: parseFloat(e.target.value)})} required />
          </div>
          <div className="form-group">
            <label>Category</label>
            <input type="text" value={newTransaction.category} onChange={(e) => setNewTransaction({...newTransaction, category: e.target.value})} required />
          </div>
          <div className="form-group">
            <label>Date</label>
            <input type="date" value={newTransaction.date} onChange={(e) => setNewTransaction({...newTransaction, date: e.target.value})} required />
          </div>
          <button type="submit" className="btn btn-primary">Add</button>
        </form>
      </div>

      <div className="card">
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid #444' }}>
              <th align="left" style={{ padding: '10px' }}>Date</th>
              <th align="left" style={{ padding: '10px' }}>Type</th>
              <th align="left" style={{ padding: '10px' }}>Category</th>
              <th align="right" style={{ padding: '10px' }}>Amount</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map(t => (
              <tr key={t.id} style={{ borderBottom: '1px solid #333' }}>
                <td style={{ padding: '10px' }}>{t.date}</td>
                <td style={{ padding: '10px', color: t.type === 'income' ? 'green' : 'red' }}>{t.type}</td>
                <td style={{ padding: '10px' }}>{t.category}</td>
                <td align="right" style={{ padding: '10px' }}>{t.currency} {t.amount.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Transactions;
