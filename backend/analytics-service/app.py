from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from cache import init_cache, close_cache
from routes.analytics import analytics_bp
import atexit

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app, origins=[Config.FRONTEND_URL], supports_credentials=True)

# Initialize cache
init_cache()

# Register blueprints
app.register_blueprint(analytics_bp, url_prefix='/analytics')

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'service': 'analytics-service'}), 200

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
    close_cache()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)