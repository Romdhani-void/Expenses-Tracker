import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Server
    PORT = int(os.getenv('PORT', 3003))
    DEBUG = os.getenv('NODE_ENV', 'development') == 'development'
    
    # MongoDB
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'expense_tracker_transactions')
    
    # JWT
    JWT_SECRET = os.getenv('JWT_SECRET', 'ExpTrk_Jwt_S3cr3t_2024_64ch_H5h_D3v_M1n1mum!!')
    
    # CORS
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
