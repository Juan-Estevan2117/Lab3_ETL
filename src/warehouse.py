import os
import subprocess
from dotenv import load_dotenv

def dump_warehouse():
    """
    Genera un archivo .sql (dump) del Data Warehouse en MySQL 
    y lo guarda en la carpeta data/warehouse.
    """
    print("📦 Generando respaldo (dump) del Data Warehouse...")
    
    # Cargar variables de entorno
    load_dotenv(override=True)
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    
    # Ruta del archivo de salida
    output_path = os.path.join('data', 'warehouse', 'warehouse_dump.sql')
    
    # Asegurar que el directorio de destino exista (aunque ya debería estar)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Comando mysqldump
    # Usamos subprocess.run para mayor control
    # --column-statistics=0 se agrega para compatibilidad con versiones antiguas de mysqldump/servidor
    # --skip-comments para un dump más limpio
    command = [
        'mysqldump',
        f'--user={DB_USER}',
        f'--password={DB_PASSWORD}',
        f'--host={DB_HOST}',
        f'--port={DB_PORT}',
        '--set-gtid-purged=OFF',
        '--column-statistics=0',
        '--add-drop-table',
        DB_NAME
    ]
    
    try:
        # Ejecutamos el comando y redirigimos la salida al archivo
        with open(output_path, 'w') as f:
            process = subprocess.run(command, stdout=f, stderr=subprocess.PIPE, text=True)
            
        if process.returncode == 0:
            print(f"✅ Dump generado exitosamente en: {output_path}")
        else:
            # mysqldump suele dar un aviso sobre contraseñas en CLI, lo cual es normal
            # pero si el código de retorno no es 0, hay un error real
            if "Using a password on the command line interface can be insecure" in process.stderr and process.returncode == 0:
                print(f"✅ Dump generado exitosamente en: {output_path}")
            else:
                print(f"❌ Error al generar el dump: {process.stderr}")
                
    except Exception as e:
        print(f"❌ Error inesperado durante el dump: {e}")

if __name__ == "__main__":
    # Si se ejecuta directamente, realiza el dump
    dump_warehouse()
