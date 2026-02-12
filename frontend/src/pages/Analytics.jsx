import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Analytics = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [period, setPeriod] = useState({ year: new Date().getFullYear(), month: new Date().getMonth() + 1 });

  useEffect(() => {
    fetchAnalytics();
  }, [period]);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const response = await api.get(`/analytics/month/${period.year}/${period.month}`);
      setAnalytics(response.data);
    } catch (err) {
      setError('Failed to fetch analytics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h2>Analytics Overview</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <div className="card" style={{ marginBottom: '20px' }}>
        <p>Displaying data for: <strong>{period.year}-{period.month}</strong></p>
      </div>

      {analytics ? (
        <div className="grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          <div className="card">
            <h3>Summary</h3>
            <p>Total Income: <span style={{ color: 'green' }}>{analytics.income?.total || 0}</span></p>
            <p>Total Expenses: <span style={{ color: 'red' }}>{analytics.expenses?.total || 0}</span></p>
            <p>Closing Balance: {analytics.closing_balance || 0}</p>
          </div>
          <div className="card">
            <h3>Category Spending</h3>
            {analytics.category_summary?.map(item => (
              <div key={item.category} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                <span>{item.category}</span>
                <span>{item.total} {item.currency}</span>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <p>No data available for this period.</p>
      )}
    </div>
  );
};

export default Analytics;
