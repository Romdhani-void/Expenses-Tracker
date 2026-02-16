import React from 'react';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { user } = useAuth();

  return (
    <div style={{ padding: '20px' }}>
      <h1>Szia, {user?.name || 'User'}!</h1>
      <p>This is your Expense Tracker Dashboard.</p>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginTop: '20px' }}>
        <div style={{ padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h3>Total Balance</h3>
          <p style={{ fontSize: '24px', fontWeight: 'bold' }}>$0.00</p>
        </div>
        <div style={{ padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h3>Monthly Income</h3>
          <p style={{ fontSize: '24px', fontWeight: 'bold', color: 'green' }}>$0.00</p>
        </div>
        <div style={{ padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h3>Monthly Expenses</h3>
          <p style={{ fontSize: '24px', fontWeight: 'bold', color: 'red' }}>$0.00</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
