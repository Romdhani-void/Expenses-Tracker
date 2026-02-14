import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Server
    PORT = int(os.getenv('PORT', 3004))
    DEBUG = os.getenv('NODE_ENV', 'development') == 'development'
    
    # Redis
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    CACHE_TTL = int(os.getenv('CACHE_TTL', 300))  # 5 minutes default
    
    # JWT
    JWT_SECRET = os.getenv('JWT_SECRET', 'ExpTrk_Jwt_S3cr3t_2024_64ch_H5h_D3v_M1n1mum!!')
    
    # CORS
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    
    # Microservices URLs
    TRANSACTION_SERVICE_URL = os.getenv('TRANSACTION_SERVICE_URL', 'http://localhost:3003')
    BUDGET_SERVICE_URL = os.getenv('BUDGET_SERVICE_URL', 'http://localhost:3002')
