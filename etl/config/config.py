# config/config.py
"""
Configuración centralizada para el ETL PostgreSQL
Este archivo contiene todas las variables de configuración necesarias
"""

# Configuración de base de datos origen
DB_ORIGEN = {
    'host': 'localhost',
    'database': 'interno_origen',
    'user': 'postgres',
    'password': 'contraseña123',
    'port': 5433
}

# Configuración de base de datos destino
DB_DESTINO = {
    'host': 'localhost',
    'database': 'interno_destino',
    'user': 'postgres',
    'password': 'contraseña123',
    'port': 5433
}

# Lista de esquemas a procesar
SCHEMAS = ['cun25436']

# Configuración de rutas
PATHS = {
    'queries': './sql/queries/',
    'inserts': './sql/inserts/',
    'logs': './logs/',
    'order_file': './sql/insert_order.txt'
}

# Configuración de rendimiento
PERFORMANCE = {
    'batch_size': 1000,          # Tamaño de lote para inserts
    'connection_pool_size': 5,   # Tamaño del pool de conexiones
    'max_retries': 3,           # Número máximo de reintentos
    'timeout': 300              # Timeout en segundos
}

# Configuración de logging
LOGGING = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S'
}