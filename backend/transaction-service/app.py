from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from database import init_db, close_db
from routes.transactions import transactions_bp
import atexit

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app, origins=[Config.FRONTEND_URL], supports_credentials=True)

# Initialize database
init_db()

# Register blueprints
app.register_blueprint(transactions_bp, url_prefix='/transactions')

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'service': 'transaction-service'}), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Cleanup on exit
@atexit.register
def cleanup():
    close_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
