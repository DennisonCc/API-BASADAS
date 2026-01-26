ejecula la app de java# Documentación de API - Sistema de Control de Pausas

## Descripción General
Esta API proporciona servicios para la gestión de empleados y el registro de pausas laborales activas. Está construida sobre **Flask** y documentada mediante **OpenAPI/Swagger**.

- **URL Base:** `http://localhost:5000/api`
- **Documentación Interactiva (Swagger UI):** `http://localhost:5000/apidocs/`
- **Formato de Respuesta:** JSON

---

## 📌 Empleados (Employees)

### 1. Listar Empleados
Obtiene la lista de todos los empleados disponibles para registrar actividades.

- **Endpoint:** `GET /empleados`
- **Respuesta Exitosa (200 OK):**
```json
[
  {
    "id": "1720123456",
    "name": "Juan Perez",
    "role": "Empleado"
  },
  {
    "id": "1720987654",
    "name": "Maria Lopez",
    "role": "Supervisor"
  }
]
```

---

## 📌 Pausas (Pauses)

### 2. Registrar Pausas (Crear)
Registra una pausa para uno o varios empleados simultáneamente.

- **Endpoint:** `POST /pausas`
- **Body (JSON):**
```json
{
  "empleados": ["1720123456", "1720987654"],
  "estado": "ALMUERZO",
  "subestado": "CANTEEN",  // Opcional
  "observacion": "Salida grupal",
  "fecha": "2024-05-20",
  "horaInicio": "12:30",
  "horaFin": "13:30",     // Opcional si la pausa sigue abierta
  "usuario": "ADMIN_SISTEMA"
}
```
- **Respuesta Exitosa (200 OK):**
```json
{
  "success": true,
  "message": "2 pausas registradas"
}
```

### 3. Consultar Historial de Pausas
Obtiene pausas filtradas por parámetros.

- **Endpoint:** `GET /pausas`
- **Parámetros (Query Params):**
    - `ci`: Filtrar por cédula (opcional, default '%')
    - `fecha_inicio`: Fecha inicio YYYY-MM-DD
    - `fecha_fin`: Fecha fin YYYY-MM-DD
- **Respuesta Exitosa (200 OK):**
```json
[
  {
    "id": 15,
    "tipo": "ALMUERZO",
    "sub_tipo": "CANTEEN",
    "empleado_id": "1720123456",
    "empleado_nombre": "Juan Perez",
    "observacion": "Salida grupal",
    "fecha": "2024-05-20",
    "hora_inicio": "12:30",
    "hora_fin": "13:30",
    "usuario_edicion": "ADMIN_SISTEMA"
  }
]
```

### 3.1. Consultar Pausas por Fecha
Busqueda directa de todas las pausas de un día específico.

- **Endpoint:** `GET /pausas/fecha/{fecha}`
- **Parámetros (URL Path):**
    - `fecha`: Fecha a consultar (YYYY-MM-DD)
- **Ejemplo:** `GET /pausas/fecha/2024-05-20`

### 4. Actualizar Pausa
Modifica una pausa existente, útil para agregar la hora de fin (cerrar pausa) o corregir observaciones.

- **Endpoint:** `PUT /pausas/{id}`
- **Body (JSON):**
```json
{
  "observacion": "Corrección de hora",
  "horaFin": "13:45",
  "usuario": "SUPERVISOR"
}
```

### 5. Eliminar Pausa
Elimina un registro de pausa.

- **Endpoint:** `DELETE /pausas/{id}`

---

## Modelos de Datos

### Objeto Empleado (`Employee`)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | String | Cédula de identidad (PK) |
| `name` | String | Nombre y Apellido concatenados |
| `role` | String | Rol del usuario (ej. Empleado) |

### Objeto Pausa (`Pause`)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | Integer | ID autoincremental de la pausa |
| `tipo` | String | Categoría (ALMUERZO, CAPACITACION, etc.) |
| `sub_tipo` | String | Subcategoría detallada |
| `empleado_id`| String | FK a Empleado |
| `fecha` | Date | Fecha del evento |
| `hora_inicio`| String | Hora formato HH:MM |
| `hora_fin` | String | Hora formato HH:MM |
