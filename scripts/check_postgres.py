import psycopg2

DB_CONFIG = {
    'host': '192.168.208.97',
    'port': 5435,
    'user': 'root',
    'password': 'root',
    'database': 'personal'
}

def test_connection():
    try:
        print(f"Intentando conectar a PostgreSQL en {DB_CONFIG['host']}:{DB_CONFIG['port']}...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Conexión exitosa a PostgreSQL")
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT version();")
            print(f"Versión de DB: {cursor.fetchone()[0]}")
            
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            print("\nTablas encontradas:")
            for table in cursor.fetchall():
                print(f"- {table[0]}")
                
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_connection()
