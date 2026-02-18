import os
import subprocess
from dotenv import load_dotenv

def dump_warehouse():
    """
    Generates a SQL dump of the MySQL Data Warehouse.

    This function executes the `mysqldump` system command to export the entire
    database schema and data into a .sql file stored in the 'data/warehouse' directory.
    
    It serves as an automated backup mechanism for the ETL pipeline.
    """
    print("📦 Generating Data Warehouse backup (dump)...")
    
    # Load Environment Variables
    load_dotenv(override=True)
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    
    # Define Output Path
    output_path = os.path.join('data', 'warehouse', 'warehouse_dump.sql')
    
    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Construct mysqldump command
    # subprocess.run is used for secure execution.
    # --column-statistics=0: Added for compatibility with older mysqldump versions.
    # --skip-comments: Generates a cleaner dump file.
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
        # Execute command and redirect stdout to the file
        with open(output_path, 'w') as f:
            process = subprocess.run(command, stdout=f, stderr=subprocess.PIPE, text=True)
            
        if process.returncode == 0:
            print(f"✅ Dump generated successfully at: {output_path}")
        else:
            # mysqldump often warns about passwords on CLI, which is expected.
            # However, if return code is non-zero, it's a real error.
            if "Using a password on the command line interface can be insecure" in process.stderr and process.returncode == 0:
                print(f"✅ Dump generated successfully at: {output_path}")
            else:
                print(f"❌ Error generating dump: {process.stderr}")
                
    except Exception as e:
        print(f"❌ Unexpected error during dump: {e}")

if __name__ == "__main__":
    # If run directly, perform the dump
    dump_warehouse()
