from flask import Blueprint, request, jsonify
from middleware.auth import authenticate_jwt
from services.calculator import AnalyticsCalculator
from cache import get_cache, set_cache
import hashlib

analytics_bp = Blueprint('analytics', __name__)

def generate_cache_key(user_id, endpoint, params):
    """Generate a cache key based on endpoint and parameters"""
    param_str = str(sorted(params.items()))
    key_str = f"{user_id}:{endpoint}:{param_str}"
    return f"analytics:{hashlib.md5(key_str.encode()).hexdigest()}"

# Get monthly summary
@analytics_bp.route('/month/<int:year>/<int:month>', methods=['GET'])
@authenticate_jwt
def get_monthly_summary(year, month):
    try:
        user_id = request.user['id']
        token = request.headers.get('Authorization').split()[1]
        
        # Build date range (needs proper implementation with calendar)
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year + 1}-01-01"
        else:
            end_date = f"{year}-{month + 1:02d}-01"
        
        # Check cache
        cache_key = generate_cache_key(user_id, 'monthly_summary', {'year': year, 'month': month})
        cached = get_cache(cache_key)
        if cached:
            return jsonify(cached), 200
        
        # Fetch data
        transactions = AnalyticsCalculator.fetch_transactions(token, user_id, start_date, end_date)
        budget = AnalyticsCalculator.fetch_budget(token, year, month)
        
        # Calculate
        income = AnalyticsCalculator.calculate_monthly_income(transactions)
        expenses = AnalyticsCalculator.calculate_monthly_expenses(transactions)
        
        opening_balance = budget['opening_balance'] if budget else 0
        closing_balance = AnalyticsCalculator.calculate_closing_balance(opening_balance, income, expenses)
        
        # Budget vs actual
        budget_comparison = AnalyticsCalculator.calculate_budget_vs_actual(budget, transactions)
        
        result = {
            'year': year,
            'month': month,
            'opening_balance': opening_balance,
            'income': income,
            'expenses': expenses,
            'closing_balance': closing_balance,
            'budget_comparison': budget_comparison,
            'transaction_count': len(transactions)
        }
        
        # Cache result
        set_cache(cache_key, result)
        
        return jsonify(result), 200
    
    except Exception as e:
        print(f"Monthly summary error: {e}")
        return jsonify({'error': 'Failed to generate monthly summary'}), 500

# Get category summary
@analytics_bp.route('/categories', methods=['GET'])
@authenticate_jwt
def get_category_summary():
    try:
        user_id = request.user['id']
        token = request.headers.get('Authorization').split()[1]
        
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Check cache
        cache_key = generate_cache_key(user_id, 'category_summary', {
            'start_date': start_date,
            'end_date': end_date
        })
        cached = get_cache(cache_key)
        if cached:
            return jsonify(cached), 200
        
        # Fetch transactions
        transactions = AnalyticsCalculator.fetch_transactions(token, user_id, start_date, end_date)
        
        # Calculate
        summary = AnalyticsCalculator.calculate_category_summary(transactions)
        
        result = {'categories': summary}
        
        # Cache result
        set_cache(cache_key, result)
        
        return jsonify(result), 200
    
    except Exception as e:
        print(f"Category summary error: {e}")
        return jsonify({'error': 'Failed to generate category summary'}), 500

# Get budget vs actual
@analytics_bp.route('/budget-vs-actual/<int:year>/<int:month>', methods=['GET'])
@authenticate_jwt
def get_budget_vs_actual(year, month):
    try:
        user_id = request.user['id']
        token = request.headers.get('Authorization').split()[1]
        
        # Check cache
        cache_key = generate_cache_key(user_id, 'budget_vs_actual', {'year': year, 'month': month})
        cached = get_cache(cache_key)
        if cached:
            return jsonify(cached), 200
        
        # Build date range
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year + 1}-01-01"
        else:
            end_date = f"{year}-{month + 1:02d}-01"
        
        # Fetch data
        transactions = AnalyticsCalculator.fetch_transactions(token, user_id, start_date, end_date)
        budget = AnalyticsCalculator.fetch_budget(token, year, month)
        
        if not budget:
            return jsonify({'error': 'No budget found for this month'}), 404
        
        # Calculate comparison
        comparison = AnalyticsCalculator.calculate_budget_vs_actual(budget, transactions)
        
        result = {
            'year': year,
            'month': month,
            'categories': comparison
        }
        
        # Cache result
        set_cache(cache_key, result)
        
        return jsonify(result), 200
    
    except Exception as e:
        print(f"Budget vs actual error: {e}")
        return jsonify({'error': 'Failed to calculate budget vs actual'}), 500

# Get real available (closing - saves)
@analytics_bp.route('/real-available/<int:year>/<int:month>', methods=['GET'])
@authenticate_jwt
def get_real_available(year, month):
    try:
        user_id = request.user['id']
        token = request.headers.get('Authorization').split()[1]
        saves = float(request.args.get('saves', 0))
        
        # Build date range
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year + 1}-01-01"
        else:
            end_date = f"{year}-{month + 1:02d}-01"
        
        # Fetch data
        transactions = AnalyticsCalculator.fetch_transactions(token, user_id, start_date, end_date)
        budget = AnalyticsCalculator.fetch_budget(token, year, month)
        
        # Calculate
        income = AnalyticsCalculator.calculate_monthly_income(transactions)
        expenses = AnalyticsCalculator.calculate_monthly_expenses(transactions)
        opening_balance = budget['opening_balance'] if budget else 0
        closing_balance = AnalyticsCalculator.calculate_closing_balance(opening_balance, income, expenses)
        real_available = AnalyticsCalculator.calculate_real_available(closing_balance, saves)
        
        return jsonify({
            'closing_balance': closing_balance,
            'designated_saves': saves,
            'real_available': real_available
        }), 200
    
    except Exception as e:
        print(f"Real available error: {e}")
        return jsonify({'error': 'Failed to calculate real available'}), 500
