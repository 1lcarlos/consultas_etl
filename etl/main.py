# main.py
"""
Archivo principal del ETL PostgreSQL
Punto de entrada para ejecutar el proceso completo
"""

import sys
import os
from datetime import datetime

# Añadir el directorio src al path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Imports locales
from config.config import DB_ORIGEN, DB_DESTINO, SCHEMAS, PATHS, PERFORMANCE
from src.etl_processor import ETLProcessor

def main():
    """
    Función principal que ejecuta el ETL completo
    """
    print("🚀 Iniciando ETL PostgreSQL...")
    print(f"🕐 Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Crear instancia del procesador ETL
    etl = ETLProcessor(
        origen_config=DB_ORIGEN,
        destino_config=DB_DESTINO,
        paths=PATHS,
        performance_config=PERFORMANCE
    )
    
    try:
        # Ejecutar el proceso ETL
        success = etl.run_etl(SCHEMAS)
        
        # Mostrar resultado final
        if success:
            print("\n🎉 PROCESO ETL COMPLETADO EXITOSAMENTE")
            print(f"📁 Log generado en: {etl.get_log_path()}")
        else:
            print("\n⚠️ PROCESO ETL COMPLETADO CON ERRORES")
            print(f"📁 Revisar log para detalles: {etl.get_log_path()}")
            
        return success
        
    except KeyboardInterrupt:
        print("\n⏹️ Proceso interrumpido por el usuario")
        etl.cleanup_resources()
        return False
        
    except Exception as e:
        print(f"\n💥 Error crítico no manejado: {str(e)}")
        etl.cleanup_resources()
        return False

if __name__ == "__main__":
    """
    Punto de entrada del script
    """
    try:
        success = main()
        # Código de salida basado en el resultado
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"💥 Error fatal: {str(e)}")
        sys.exit(1)