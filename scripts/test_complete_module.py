import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

def run_comprehensive_tests():
    print(f"--- Iniciando Pruebas Completas del Módulo 'Tiempos Fuera' en {BASE_URL} ---")
    
    # 1. Obtener Empleados
    print("\n1. Test GET /api/empleados")
    resp = requests.get(f"{BASE_URL}/api/empleados")
    if resp.status_code == 200:
        print("✅ Éxito")
        empleados = resp.json()
        if len(empleados) > 0:
            test_ci = empleados[0]['id']
            print(f"   Usando CI para pruebas: {test_ci}")
        else:
            print("   ⚠️ No hay empleados en la BD")
            return
    else:
        print(f"❌ Error: {resp.text}")
        return

    # 2. Crear una Pausa (POST)
    print("\n2. Test POST /api/pausas")
    payload = {
        "estado": "REUNION_TEST",
        "subestado": "SUB_TEST",
        "empleados": [test_ci],
        "observacion": "TEST AUTOMATICO COMPLETO",
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "horaInicio": "09:00",
        "horaFin": "10:00",
        "usuario": "TESTER_BOT"
    }
    resp = requests.post(f"{BASE_URL}/api/pausas", json=payload)
    if resp.status_code == 200:
        print("✅ Pausa creada")
    else:
        print(f"❌ Error: {resp.text}")
        return

    # 3. Listar y Buscar Pausa (GET)
    print("\n3. Test GET /api/pausas (Buscar la pausa creada)")
    resp = requests.get(f"{BASE_URL}/api/pausas", params={"ci": test_ci})
    pausas = resp.json()
    if resp.status_code == 200 and len(pausas) > 0:
        target = pausas[0]
        id_pausa = target['id']
        print(f"✅ Pausa encontrada. ID: {id_pausa}")
    else:
        print(f"❌ Error: No se encontró la pausa creada. {resp.text}")
        return

    # 4. Actualizar Pausa (PUT)
    print(f"\n4. Test PUT /api/pausas/{id_pausa}")
    update_payload = {
        "observacion": "OBSERVACION ACTUALIZADA POR BOT",
        "horaFin": "11:30",
        "usuario": "TESTER_BOT_EDIT"
    }
    resp = requests.put(f"{BASE_URL}/api/pausas/{id_pausa}", json=update_payload)
    if resp.status_code == 200:
        print("✅ Pausa actualizada")
    else:
        print(f"❌ Error: {resp.text}")

    # 5. Eliminar Pausa (DELETE)
    print(f"\n5. Test DELETE /api/pausas/{id_pausa}")
    resp = requests.delete(f"{BASE_URL}/api/pausas/{id_pausa}")
    if resp.status_code == 200:
        print("✅ Pausa eliminada")
    else:
        print(f"❌ Error: {resp.text}")

    print("\n--- Pruebas Finalizadas ---")

if __name__ == "__main__":
    try:
        run_comprehensive_tests()
    except Exception as e:
        print(f"Error de conexión: {e}. Asegúrate de que Flask esté corriendo.")
