from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime
from database import get_db
from middleware.auth import authenticate_jwt
from models.transaction import Transaction

transactions_bp = Blueprint('transactions', __name__)

# Get all transactions
@transactions_bp.route('/', methods=['GET'])
@authenticate_jwt
def get_transactions():
    try:
        db = get_db()
        user_id = request.user['id']
        
        # Query parameters for filtering
        transaction_type = request.args.get('type')  # 'income' or 'expense'
        category = request.args.get('category')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = int(request.args.get('limit', 100))
        skip = int(request.args.get('skip', 0))
        
        # Build query
        query = {'user_id': user_id}
        
        if transaction_type:
            query['type'] = transaction_type
        
        if category:
            query['category'] = category
        
        if start_date or end_date:
            query['date'] = {}
            if start_date:
                query['date']['$gte'] = start_date
            if end_date:
                query['date']['$lte'] = end_date
        
        # Execute query
        transactions = list(
            db.transactions.find(query)
            .sort('date', -1)
            .skip(skip)
            .limit(limit)
        )
        
        # Convert to JSON
        for trans in transactions:
            trans['_id'] = str(trans['_id'])
        
        total = db.transactions.count_documents(query)
        
        return jsonify({
            'transactions': transactions,
            'total': total,
            'limit': limit,
            'skip': skip
        }), 200
    
    except Exception as e:
        print(f"Get transactions error: {e}")
        return jsonify({'error': 'Failed to fetch transactions'}), 500

# Get transaction by ID
@transactions_bp.route('/<transaction_id>', methods=['GET'])
@authenticate_jwt
def get_transaction(transaction_id):
    try:
        db = get_db()
        user_id = request.user['id']
        
        transaction = db.transactions.find_one({
            '_id': ObjectId(transaction_id),
            'user_id': user_id
        })
        
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        transaction['_id'] = str(transaction['_id'])
        return jsonify({'transaction': transaction}), 200
    
    except Exception as e:
        print(f"Get transaction error: {e}")
        return jsonify({'error': 'Failed to fetch transaction'}), 500

# Create transaction
@transactions_bp.route('/', methods=['POST'])
@authenticate_jwt
def create_transaction():
    try:
        data = request.get_json()
        user_id = request.user['id']
        
        # Validate
        is_valid, error = Transaction.validate_transaction(data)
        if not is_valid:
            return jsonify({'error': error}), 400
        
        # Create transaction
        transaction = Transaction.create_transaction(
            user_id=user_id,
            transaction_type=data['type'],
            amount=data['amount'],
            currency=data['currency'],
            category=data['category'],
            date=data['date'],
            notes=data.get('notes')
        )
        
        # Insert to database
        db = get_db()
        result = db.transactions.insert_one(transaction)
        
        transaction['_id'] = str(result.inserted_id)
        
        return jsonify({
            'message': 'Transaction created successfully',
            'transaction': transaction
        }), 201
    
    except Exception as e:
        print(f"Create transaction error: {e}")
        return jsonify({'error': 'Failed to create transaction'}), 500

# Update transaction
@transactions_bp.route('/<transaction_id>', methods=['PUT'])
@authenticate_jwt
def update_transaction(transaction_id):
    try:
        data = request.get_json()
        user_id = request.user['id']
        db = get_db()
        
        # Check ownership
        transaction = db.transactions.find_one({
            '_id': ObjectId(transaction_id),
            'user_id': user_id
        })
        
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        # Build update data
        update_data = {}
        if 'amount' in data:
            update_data['amount'] = float(data['amount'])
        if 'currency' in data:
            update_data['currency'] = data['currency']
        if 'category' in data:
            update_data['category'] = data['category']
        if 'date' in data:
            update_data['date'] = data['date']
        if 'notes' in data:
            update_data['notes'] = data['notes']
        if 'type' in data:
            update_data['type'] = data['type']
        
        update_data['updated_at'] = datetime.utcnow().isoformat()
        
        # Update
        db.transactions.update_one(
            {'_id': ObjectId(transaction_id)},
            {'$set': update_data}
        )
        
        # Get updated transaction
        updated = db.transactions.find_one({'_id': ObjectId(transaction_id)})
        updated['_id'] = str(updated['_id'])
        
        return jsonify({
            'message': 'Transaction updated successfully',
            'transaction': updated
        }), 200
    
    except Exception as e:
        print(f"Update transaction error: {e}")
        return jsonify({'error': 'Failed to update transaction'}), 500

# Delete transaction
@transactions_bp.route('/<transaction_id>', methods=['DELETE'])
@authenticate_jwt
def delete_transaction(transaction_id):
    try:
        user_id = request.user['id']
        db = get_db()
        
        result = db.transactions.delete_one({
            '_id': ObjectId(transaction_id),
            'user_id': user_id
        })
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Transaction not found'}), 404
        
        return jsonify({'message': 'Transaction deleted successfully'}), 200
    
    except Exception as e:
        print(f"Delete transaction error: {e}")
        return jsonify({'error': 'Failed to delete transaction'}), 500

# Get summary by category
@transactions_bp.route('/summary/by-category', methods=['GET'])
@authenticate_jwt
def get_summary_by_category():
    try:
        db = get_db()
        user_id = request.user['id']
        
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        transaction_type = request.args.get('type')  # Optional: 'income' or 'expense'
        
        # Build match stage
        match_stage = {'user_id': user_id}
        
        if start_date or end_date:
            match_stage['date'] = {}
            if start_date:
                match_stage['date']['$gte'] = start_date
            if end_date:
                match_stage['date']['$lte'] = end_date
        
        if transaction_type:
            match_stage['type'] = transaction_type
        
        # Aggregate
        pipeline = [
            {'$match': match_stage},
            {
                '$group': {
                    '_id': '$category',
                    'total': {'$sum': '$amount'},
                    'count': {'$sum': 1},
                    'currency': {'$first': '$currency'}
                }
            },
            {'$sort': {'total': -1}}
        ]
        
        results = list(db.transactions.aggregate(pipeline))
        
        summary = []
        for result in results:
            summary.append({
                'category': result['_id'],
                'total': result['total'],
                'count': result['count'],
                'currency': result['currency']
            })
        
        return jsonify({'summary': summary}), 200
    
    except Exception as e:
        print(f"Get summary error: {e}")
        return jsonify({'error': 'Failed to generate summary'}), 500
