import pymysql

DB_CONFIG = {
    'host': '192.168.208.97',
    'port': 3307,
    'user': 'root',
    'password': 'root',
    'database': 'personal'
}

def list_tables():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            print("Tablas en DB 'personal':")
            for table in cursor.fetchall():
                print(f"- {table[0]}")
    except Exception as e:
        print(e)
    finally:
        conn.close()

if __name__ == '__main__':
    list_tables()
