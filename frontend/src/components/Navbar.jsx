import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav style={{ padding: '10px 20px', backgroundColor: '#333', color: 'white', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <h3>Expense Tracker</h3>
      <div>
        <Link to="/" style={{ color: 'white', marginRight: '15px' }}>Dashboard</Link>
        <Link to="/budgets" style={{ color: 'white', marginRight: '15px' }}>Budgets</Link>
        <Link to="/transactions" style={{ color: 'white', marginRight: '15px' }}>Transactions</Link>
        <Link to="/analytics" style={{ color: 'white', marginRight: '15px' }}>Analytics</Link>
        {user ? (
          <button onClick={handleLogout} style={{ border: 'none', background: 'transparent', color: 'white', cursor: 'pointer' }}>Logout</button>
        ) : (
          <Link to="/login" style={{ color: 'white' }}>Login</Link>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
