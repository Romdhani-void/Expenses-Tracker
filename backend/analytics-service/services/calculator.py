import requests
from config import Config
from datetime import datetime

class AnalyticsCalculator:
    """Business logic for analytics calculations"""
    
    @staticmethod
    def fetch_transactions(token, user_id, start_date=None, end_date=None, transaction_type=None):
        """Fetch transactions from Transaction Service"""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            params = {}
            
            if start_date:
                params['start_date'] = start_date
            if end_date:
                params['end_date'] = end_date
            if transaction_type:
                params['type'] = transaction_type
            
            params['limit'] = 1000  # Get all for calculations
            
            response = requests.get(
                f"{Config.TRANSACTION_SERVICE_URL}/transactions/",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get('transactions', [])
            return []
        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return []
    
    @staticmethod
    def fetch_budget(token, year, month):
        """Fetch budget from Budget Service"""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(
                f"{Config.BUDGET_SERVICE_URL}/budgets/month/{year}/{month}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get('budget')
            return None
        except Exception as e:
            print(f"Error fetching budget: {e}")
            return None
    
    @staticmethod
    def calculate_monthly_expenses(transactions):
        """Calculate total expenses for a month"""
        expenses = [t for t in transactions if t['type'] == 'expense']
        
        # Group by currency
        by_currency = {}
        for expense in expenses:
            currency = expense['currency']
            if currency not in by_currency:
                by_currency[currency] = 0
            by_currency[currency] += expense['amount']
        
        total = sum(expenses for expenses in by_currency.values())
        
        return {
            'total': total,
            'by_currency': by_currency,
            'count': len(expenses)
        }
    
    @staticmethod
    def calculate_monthly_income(transactions):
        """Calculate total income for a month"""
        income = [t for t in transactions if t['type'] == 'income']
        
        # Group by currency
        by_currency = {}
        for inc in income:
            currency = inc['currency']
            if currency not in by_currency:
                by_currency[currency] = 0
            by_currency[currency] += inc['amount']
        
        total = sum(income for income in by_currency.values())
        
        return {
            'total': total,
            'by_currency': by_currency,
            'count': len(income)
        }
    
    @staticmethod
    def calculate_closing_balance(opening_balance, income, expenses):
        """Calculate closing balance"""
        closing = opening_balance + income['total'] - expenses['total']
        return closing
    
    @staticmethod
    def calculate_real_available(closing_balance, saves):
        """Calculate real available money (closing - designated saves)"""
        return closing_balance - saves
    
    @staticmethod
    def calculate_budget_vs_actual(budget, transactions):
        """Compare budget vs actual spending by category"""
        if not budget or 'categories' not in budget:
            return []
        
        # Calculate actual spending by category
        expenses = [t for t in transactions if t['type'] == 'expense']
        actual_by_category = {}
        
        for expense in expenses:
            category = expense['category']
            if category not in actual_by_category:
                actual_by_category[category] = {'total': 0, 'count': 0}
            actual_by_category[category]['total'] += expense['amount']
            actual_by_category[category]['count'] += 1
        
        # Compare with budget
        comparison = []
        for category in budget['categories']:
            cat_name = category['name']
            planned = category['planned_amount']
            actual = actual_by_category.get(cat_name, {'total': 0, 'count': 0})['total']
            difference = planned - actual
            percentage = (actual / planned * 100) if planned > 0 else 0
            
            comparison.append({
                'category': cat_name,
                'planned': planned,
                'actual': actual,
                'difference': difference,
                'percentage_used': round(percentage, 2),
                'over_budget': actual > planned,
                'currency': category['currency']
            })
        
        return comparison
    
    @staticmethod
    def calculate_category_summary(transactions):
        """Calculate spending summary by category"""
        expenses = [t for t in transactions if t['type'] == 'expense']
        
        by_category = {}
        for expense in expenses:
            category = expense['category']
            if category not in by_category:
                by_category[category] = {
                    'total': 0,
                    'count': 0,
                    'currency': expense['currency'],
                    'transactions': []
                }
            by_category[category]['total'] += expense['amount']
            by_category[category]['count'] += 1
            by_category[category]['transactions'].append({
                'date': expense['date'],
                'amount': expense['amount'],
                'notes': expense.get('notes', '')
            })
        
        # Convert to list and sort by total
        summary = [
            {
                'category': cat,
                'total': data['total'],
                'count': data['count'],
                'currency': data['currency'],
                'average': round(data['total'] / data['count'], 2),
                'transactions': data['transactions']
            }
            for cat, data in by_category.items()
        ]
        
        summary.sort(key=lambda x: x['total'], reverse=True)
        return summary
    
    @staticmethod
    def calculate_monthly_trend(transactions_by_month):
        """Calculate spending trends across months"""
        trend = []
        
        for month_data in transactions_by_month:
            income = AnalyticsCalculator.calculate_monthly_income(month_data['transactions'])
            expenses = AnalyticsCalculator.calculate_monthly_expenses(month_data['transactions'])
            
            trend.append({
                'month': month_data['month'],
                'year': month_data['year'],
                'income': income['total'],
                'expenses': expenses['total'],
                'net': income['total'] - expenses['total']
            })
        
        return trend
