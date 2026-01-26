import requests
import json
import time

BASE_URL = "http://localhost:5000/api"

def print_result(name, response):
    status = "✅ PASS" if response.status_code in [200, 201] else "❌ FAIL"
    print(f"\n[{status}] {name}")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    return response

def test_endpoints():
    print("=== INICIANDO PRUEBAS DE ENDPOINTS ===")
    
    # 1. GET Empleados
    resp = print_result("1. GET /empleados", requests.get(f"{BASE_URL}/empleados"))
    if resp.status_code != 200 or not resp.json():
        print("No se pueden continuar las pruebas sin empleados.")
        return
    
    # Tomar el primer empleado para las pruebas
    empleado_id = resp.json()[0]['id'].strip()
    print(f"--> Usando Empleado ID: {empleado_id}")

    # 2. POST Pausa
    new_pause = {
        "empleados": [empleado_id],
        "estado": "TEST_AUTO",
        "subestado": "ANTIGRAVITY",
        "observacion": "Prueba automatizada de integridad",
        "fecha": "2026-01-19",
        "horaInicio": "10:00",
        "usuario": "TEST_SCRIPT"
    }
    resp = print_result("2. POST /pausas", requests.post(f"{BASE_URL}/pausas", json=new_pause))
    
    # Si falló el post, intentamos ver por qué, pero no podemos seguir con PUT/DELETE de este ID específico fácilmente sin saber cual se creó.
    # Asumimos que si fue exitoso, buscaremos la última pausa creada.
    
    time.sleep(1) 

    # 3. GET Pausas (Buscar la que acabamos de crear)
    # Filtramos por fecha y empleado para encontrarla
    resp = print_result(f"3. GET /pausas (Filter by ID {empleado_id})", 
                        requests.get(f"{BASE_URL}/pausas?ci={empleado_id}&fecha_inicio=2026-01-19"))
    
    pausas = resp.json()
    if not pausas:
        print("❌ No se encontró la pausa creada.")
        return

    # Buscar la última
    target_pause = pausas[-1]
    pause_id = target_pause['id']
    print(f"--> Pausa Creada ID: {pause_id}")

    # 4. PUT Pausa (Cerrar/Actualizar)
    update_data = {
        "observacion": "Prueba automatizada - ACTUALIZADA",
        "horaFin": "11:00",
        "usuario": "TEST_SCRIPT"
    }
    print_result(f"4. PUT /pausas/{pause_id}", requests.put(f"{BASE_URL}/pausas/{pause_id}", json=update_data))

    # 5. DELETE Pausa
    print_result(f"5. DELETE /pausas/{pause_id}", requests.delete(f"{BASE_URL}/pausas/{pause_id}"))

    print("\n=== PRUEBAS FINALIZADAS ===")

if __name__ == "__main__":
    test_endpoints()
