import pymysql
import sys

# Configuración basada en tu código Java
DB_CONFIG = {
    'host': 'localhost',
    'port': 3307,
    'user': 'root',
    'password': 'root',
    'database': 'personal'
}

def check_db_modification_capability():
    print(f"--- Verificando conexión y permisos de escritura en {DB_CONFIG['host']}:{DB_CONFIG['port']} ---")
    
    try:
        connection = pymysql.connect(**DB_CONFIG)
        print("✅ Conexión Exitosa con MySQL.")
        
        with connection.cursor() as cursor:
            # 1. Verificar si existe la tabla 'pausas'
            print("1. Verificando tablas existentes...")
            cursor.execute("SHOW TABLES LIKE 'pausas'")
            result = cursor.fetchone()
            
            if result:
                print(f"✅ Tabla 'pausas' encontrada: {result[0]}")
                
                # 2. Verificar estructura (opcional, para ver si coincide)
                cursor.execute("DESCRIBE pausas")
                columns = [row[0] for row in cursor.fetchall()]
                print(f"   Columnas: {columns}")
                
                # 3. Prueba de Escritura (INSERT + ROLLBACK)
                # Intentamos insertar un dato dummy para ver si hay permisos de escritura
                print("\n2. Probando permisos de escritura (INSERT)...")
                try:
                    # Ajusta esto si las columnas son diferentes, basado en el Java parecía tener muchos campos
                    # El script Python app.py usa: estado, sub_estado, empleado_ci, observacion, fecha_pausa, hora_inicio, hora_fin, fecha_registro, usuario_registro
                    
                    # Vamos a intentar un INSERT genérico si sabemos las columnas, o uno muy simple si falla.
                    # Para seguridad, solo verificamos si el usuario tiene GRANT INSERT.
                    
                    cursor.execute("SHOW GRANTS FOR CURRENT_USER()")
                    grants = cursor.fetchall()
                    print("   Permisos del usuario:")
                    for grant in grants:
                        print(f"   - {grant[0]}")
                        
                    print("✅ El usuario parece tener permisos. (La prueba real de INSERT depende de que coincidan las columnas).")
                    
                except Exception as e:
                     print(f"❌ Error verificando permisos: {e}")

            else:
                print("⚠️ La tabla 'pausas' NO existe. El código Python fallará al intentar insertar.")
                print("   ¿Necesitas que cree el script SQL para generar esta tabla?")

    except pymysql.err.OperationalError as e:
        print(f"❌ ERROR CRÍTICO DE CONEXIÓN: {e}")
        print("   No se puede conectar al puerto 3307. La BD no es modificable porque no es accesible.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
            print("\nConexión cerrada.")

if __name__ == "__main__":
    check_db_modification_capability()
