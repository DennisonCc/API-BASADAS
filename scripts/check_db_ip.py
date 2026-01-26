import pymysql
import sys

# INTENTO 2: Verificar conexión directa a la IP de WSL
# Asumiendo que WSL no tiene el puerto forwarded a localhost, intentamos directo a la IP

DB_CONFIG = {
    'host': '192.168.208.97', # IP detectada de WSL
    'port': 3306, # Puerto interno en linux suele ser el default si no se cambió
    'user': 'root',
    'password': 'root',
    'database': 'personal'
}

def check_db_ip():
    print(f"--- Prueba Directa a IP WSL: {DB_CONFIG['host']} ---")
    
    # Probamos puerto 3306 (default interno) y 3307 (por si acaso lo cambiaron dentro)
    ports_to_try = [3306, 3307]
    
    for port in ports_to_try:
        print(f"\nIntentando conectar al puerto {port}...")
        try:
            DB_CONFIG['port'] = port
            connection = pymysql.connect(**DB_CONFIG)
            print(f"✅ ¡ÉXITO! Conexión lograda al puerto {port}.")
            
            with connection.cursor() as cursor:
                cursor.execute("SHOW TABLES LIKE 'pausas'")
                result = cursor.fetchone()
                if result:
                    print(f"✅ Tabla 'pausas' detectada. SISTEMA LISTO PARA MODIFICAR BD.")
                else:
                    print(f"⚠️ Conexión OK, pero tabla 'pausas' no encontrada.")
            
            connection.close()
            return # Exit success
            
        except Exception as e:
            print(f"❌ Falló conexión al puerto {port}: {e}")

if __name__ == "__main__":
    check_db_ip()
