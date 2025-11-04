# src/database_manager.py
"""
Gestor de conexiones a PostgreSQL con pool de conexiones
Maneja las conexiones de manera eficiente y segura
"""

import psycopg2
from psycopg2 import pool, sql
from psycopg2.extras import RealDictCursor
import logging
from typing import Dict, Any, Optional
from contextlib import contextmanager

class DatabaseManager:
    """
    Clase para manejar conexiones a PostgreSQL de manera eficiente.
    Utiliza pools de conexión para optimizar el rendimiento.
    """
    
    def __init__(self, db_config: Dict[str, Any], pool_size: int = 5):
        """
        Inicializa el gestor de base de datos
        
        Args:
            db_config: Diccionario con parámetros de conexión
            pool_size: Tamaño del pool de conexiones
        """
        self.db_config = db_config
        self.pool_size = pool_size
        self.connection_pool = None
        self.logger = logging.getLogger(__name__)
        
    def create_connection_pool(self) -> bool:
        """
        Crea un pool de conexiones a PostgreSQL
        
        Returns:
            bool: True si la conexión fue exitosa, False en caso contrario
        """
        try:
            # Crear el pool de conexiones
            self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=self.pool_size,
                host=self.db_config['host'],
                database=self.db_config['database'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                port=self.db_config['port'],
                cursor_factory=RealDictCursor  # Para obtener resultados como diccionarios
            )
            
            # Probar la conexión
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute('SELECT version();')
                    version = cursor.fetchone()
                    
            self.logger.info(f"✅ Conexión exitosa a {self.db_config['database']} en {self.db_config['host']}")
            self.logger.info(f"📊 Versión PostgreSQL: {version['version']}")
            return True
            
        except psycopg2.OperationalError as e:
            self.logger.error(f"❌ Error de conexión a {self.db_config['database']}: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"❌ Error inesperado al conectar a {self.db_config['database']}: {str(e)}")
            return False
    
    @contextmanager
    def get_connection(self):
        """
        Context manager para obtener conexiones del pool de manera segura
        Garantiza que las conexiones se devuelvan al pool correctamente
        """
        connection = None
        try:
            if not self.connection_pool:
                raise Exception("Pool de conexiones no inicializado")
                
            # Obtener conexión del pool
            connection = self.connection_pool.getconn()
            if connection:
                yield connection
            else:
                raise Exception("No se pudo obtener conexión del pool")
                
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection and self.connection_pool:
                # Devolver conexión al pool
                self.connection_pool.putconn(connection)
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> list:
        """
        Ejecuta una consulta SELECT y retorna los resultados
        
        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros para la consulta (opcional)
            
        Returns:
            list: Lista de diccionarios con los resultados
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    results = cursor.fetchall()
                    
            self.logger.info(f"✅ Consulta ejecutada exitosamente. Filas obtenidas: {len(results)}")
            return results
            
        except Exception as e:
            self.logger.error(f"❌ Error ejecutando consulta: {str(e)}")
            raise e
    
    def execute_insert(self, query: str, data: Optional[list] = None) -> int:
        """
        Ejecuta un INSERT y retorna el número de filas afectadas
        
        Args:
            query: Consulta INSERT a ejecutar
            data: Datos para insert masivo (opcional)
            
        Returns:
            int: Número de filas insertadas
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    if data:
                        # Insert masivo para mejor rendimiento
                        cursor.executemany(query, data)
                    else:
                        cursor.execute(query)
                    
                    rows_affected = cursor.rowcount
                    conn.commit()
                    
            self.logger.info(f"✅ Insert ejecutado exitosamente. Filas insertadas: {rows_affected}")
            return rows_affected
            
        except Exception as e:
            self.logger.error(f"❌ Error ejecutando insert: {str(e)}")
            raise e
    
    def create_temp_table_from_data(self, table_name: str, data: list, schema: str = 'public') -> bool:
        """
        Crea una tabla temporal a partir de datos
        
        Args:
            table_name: Nombre de la tabla temporal
            data: Datos para insertar
            schema: Esquema donde crear la tabla
            
        Returns:
            bool: True si fue exitoso
        """
        if not data:
            self.logger.warning(f"⚠️ No hay datos para crear tabla {table_name}")
            return False
            
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Crear tabla temporal basada en la estructura del primer registro
                    first_row = data[0]
                    columns = []
                    
                    for key, value in first_row.items():
                        if isinstance(value, int):
                            col_type = 'INTEGER'
                        elif isinstance(value, float):
                            col_type = 'NUMERIC'
                        elif isinstance(value, bool):
                            col_type = 'BOOLEAN'
                        else:
                            col_type = 'TEXT'
                        
                        columns.append(f'"{key}" {col_type}')
                    
                    # Crear tabla temporal
                    create_query = f"""
                    CREATE TEMP TABLE {table_name} (
                        {', '.join(columns)}
                    )
                    """
                    
                    cursor.execute(create_query)
                    
                    # Insertar datos en lotes para eficiencia
                    batch_size = 1000
                    for i in range(0, len(data), batch_size):
                        batch = data[i:i + batch_size]
                        values = []
                        
                        for row in batch:
                            row_values = [row[key] for key in first_row.keys()]
                            values.append(row_values)
                        
                        # Preparar query de insert
                        placeholders = ','.join(['%s'] * len(first_row.keys()))
                        insert_query = f"""
                        INSERT INTO {table_name} ({','.join(f'"{k}"' for k in first_row.keys())})
                        VALUES ({placeholders})
                        """
                        
                        cursor.executemany(insert_query, values)
                    
                    conn.commit()
                    
            self.logger.info(f"✅ Tabla temporal {table_name} creada con {len(data)} registros")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error creando tabla temporal {table_name}: {str(e)}")
            raise e
    
    def drop_temp_table(self, table_name: str) -> bool:
        """
        Elimina una tabla temporal
        
        Args:
            table_name: Nombre de la tabla a eliminar
            
        Returns:
            bool: True si fue exitoso
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                    conn.commit()
                    
            self.logger.info(f"🗑️ Tabla temporal {table_name} eliminada")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error eliminando tabla temporal {table_name}: {str(e)}")
            return False
    
    def close_pool(self):
        """
        Cierra el pool de conexiones
        """
        if self.connection_pool:
            self.connection_pool.closeall()
            self.logger.info("🔒 Pool de conexiones cerrado")
    
    def __del__(self):
        """
        Destructor para asegurar que se cierren las conexiones
        """
        self.close_pool()