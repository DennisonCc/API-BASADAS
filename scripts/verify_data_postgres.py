import psycopg2

DB_CONFIG = {
    'host': '192.168.208.97',
    'port': 5435,
    'user': 'root',
    'password': 'root',
    'database': 'personal'
}

def verify_data():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            # Check counts
            tables = ['area', 'empleado', 'turno', 'pausas', 'firma']
            print("--- Conteo de registros en PostgreSQL ---")
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"Tabla '{table}': {count} registros")
            
            # Show a few records from pausas (the official ones from the SQL file)
            print("\n--- Muestra de Pausas Existentes (Top 5) ---")
            cursor.execute("""
                SELECT p.id_pausa, p.tipo_pausa, p.empleado_pausa, e.nombres, e.apellidos 
                FROM pausas p
                JOIN empleado e ON p.empleado_pausa = e.ci
                LIMIT 5
            """)
            for row in cursor.fetchall():
                print(f"ID: {row[0]} | Tipo: {row[1]} | Empleado: {row[3]} {row[4]} ({row[2]})")

        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    verify_data()
