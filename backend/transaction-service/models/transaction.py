from datetime import datetime

class Transaction:
    """Transaction model schema"""
    
    @staticmethod
    def create_transaction(user_id, transaction_type, amount, currency, category, date, notes=None):
        """Create a transaction document"""
        return {
            'user_id': user_id,
            'type': transaction_type,  # 'income' or 'expense'
            'amount': float(amount),
            'currency': currency,
            'category': category,
            'date': date,  # ISO format string
            'notes': notes,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def validate_transaction(data):
        """Validate transaction data"""
        required_fields = ['type', 'amount', 'currency', 'category', 'date']
        
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        if data['type'] not in ['income', 'expense']:
            return False, "Type must be either 'income' or 'expense'"
        
        try:
            amount = float(data['amount'])
            if amount <= 0:
                return False, "Amount must be greater than 0"
        except ValueError:
            return False, "Invalid amount format"
        
        if len(data['currency']) != 3:
            return False, "Currency must be a 3-letter code"
        
        try:
            datetime.fromisoformat(data['date'].replace('Z', '+00:00'))
        except ValueError:
            return False, "Invalid date format. Use ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)"
        
        return True, None
    
    @staticmethod
    def to_json(transaction):
        """Convert MongoDB document to JSON"""
        if transaction:
            transaction['_id'] = str(transaction['_id'])
        return transaction
