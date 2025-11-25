# config/config.py
"""
Configuración centralizada para el ETL PostgreSQL
Este archivo contiene todas las variables de configuración necesarias
"""

# Configuración de base de datos origen
DB_ORIGEN = {
    'host': 'localhost',
    'database': 'Septiembre',
    'user': 'postgres',
    'password': 'Jacobo1234',
    'port': 5434
}

# Configuración de base de datos destino
DB_DESTINO = {
    'host': 'localhost',
    'database': 'modelo_interno',
    'user': 'postgres',
    'password': 'Jacobo1234',
    'port': 5434
}

# Lista de esquemas a procesar
SCHEMAS = ['cun25436']#,'cun25797','cun25489']
#SCHEMAS = ['cun25489']

# Configuración de rutas
PATHS = {
    'queries': 'C:\ETL_modelo_interno\consultas_etl\etl\sql\queries',
    'inserts': 'C:\ETL_modelo_interno\consultas_etl\etl\sql\inserts',
    'logs': 'C:\ETL_modelo_interno\consultas_etl\logs',
    'order_file': 'C:\ETL_modelo_interno\consultas_etl\etl\sql\insert_order.txt'
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