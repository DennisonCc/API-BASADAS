import urllib.request
import json
import ssl

# Bypass SSL verify if needed (for localhost usually not needed but good practice for scripts)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "http://localhost:5000/api/pausas"
data = {
    "empleados": ["1003484936"],
    "estado": "PRUEBA",
    "subestado": "TEST_SCRIPT",
    "observacion": "Post de prueba generado por Antigravity",
    "fecha": "2026-01-19",
    "horaInicio": "12:30",
    "usuario": "ANTIGRAVITY"
}

print(f"Enviando POST a {url} con datos: {data}")

try:
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, context=ctx) as f:
        print("Status Code:", f.getcode())
        print("Response:", f.read().decode('utf-8'))
except Exception as e:
    print("Error:", e)
    # Read error body if available
    if hasattr(e, 'read'):
        print("Error Body:", e.read().decode('utf-8'))
