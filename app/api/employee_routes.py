from flask import Blueprint, jsonify
from app.services.employee_service import EmployeeService

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/api/empleados', methods=['GET'])
def get_empleados():
    """
    Obtener lista de empleados activos
    Recupera todos los empleados registrados que pueden registrar pausas.
    ---
    tags:
      - Empleados
    responses:
      200:
        description: Lista de empleados recuperada exitosamente
        schema:
          type: array
          items:
            type: object
            required:
              - id
              - name
              - role
            properties:
              id:
                type: string
                description: Cédula de Identidad del empleado
                example: "1720123456"
              name:
                type: string
                description: Nombre completo del empleado
                example: "Juan Pérez"
              role:
                type: string
                description: Rol del empleado en el sistema
                example: "Analista"
      500:
        description: Error interno del servidor
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Error de conexión con la base de datos"
    """
    try:
        employees = EmployeeService.get_employees()
        return jsonify(employees)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
