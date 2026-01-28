from flask import Blueprint, request, jsonify
from app.services.pause_service import PauseService

pause_bp = Blueprint('pause', __name__)

@pause_bp.route('/api/pausas', methods=['GET'])
def get_pausas():
    """
    Obtener historial de pausas
    Permite filtrar pausas por empleado y rango de fechas.
    ---
    tags:
      - Pausas
    parameters:
      - name: ci
        in: query
        type: string
        description: Cédula del empleado para filtrar (búsqueda parcial o exacta)
        default: '%'
      - name: fecha_inicio
        in: query
        type: string
        format: date
        description: Fecha de inicio del filtro (YYYY-MM-DD)
      - name: fecha_fin
        in: query
        type: string
        format: date
        description: Fecha de fin del filtro (YYYY-MM-DD)
    responses:
      200:
        description: Lista de pausas encontradas
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: Identificador único de la pausa
              tipo:
                type: string
                description: Categoría principal de la pausa
                example: "ALMUERZO"
              sub_tipo:
                type: string
                description: Subcategoría o detalle de la pausa
              empleado_id:
                type: string
                description: Cédula del empleado
              empleado_nombre:
                type: string
                description: Nombre completo del empleado
              observacion:
                type: string
                description: Notas adicionales
              fecha:
                type: string
                format: date
                description: Fecha del registro
              hora_inicio:
                type: string
                description: Hora de inicio (HH:MM)
              hora_fin:
                type: string
                description: Hora de finalización (HH:MM)
              usuario_edicion:
                type: string
                description: Usuario que realizó la última modificación
      500:
        description: Error interno del servidor
    """
    try:
        ci = request.args.get('ci', '%')
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        
        pausas = PauseService.get_pausas(ci, fecha_inicio, fecha_fin)
        return jsonify(pausas)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@pause_bp.route('/api/pausas/fecha/<string:fecha>', methods=['GET'])
def get_pausas_por_fecha(fecha):
    """
    Obtener pausas por fecha específica
    Busca todas las pausas registradas en un día en particular.
    ---
    tags:
      - Pausas
    parameters:
      - name: fecha
        in: path
        type: string
        required: true
        format: date
        description: Fecha a consultar (YYYY-MM-DD)
    responses:
      200:
        description: Lista de pausas del día
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              tipo:
                type: string
              empleado_nombre:
                type: string
              fecha:
                type: string
      500:
        description: Error interno
    """
    try:
        # Reutilizamos el servicio pasando la misma fecha como inicio y fin
        pausas = PauseService.get_pausas(fecha_inicio=fecha, fecha_fin=fecha)
        return jsonify(pausas)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@pause_bp.route('/api/pausas', methods=['POST'])
def create_pausas():
    """
    Registrar nuevas pausas
    Crea registros de pausa para uno o varios empleados simultáneamente.
    ---
    tags:
      - Pausas
    parameters:
      - name: body
        in: body
        required: true
        description: Datos de la pausa a registrar
        schema:
          type: object
          required:
            - empleados
            - estado
            - fecha
            - horaInicio
          properties:
            empleados:
              type: array
              description: Lista de cédulas de identidad de los empleados
              items:
                type: string
                example: "1720555555"
            estado:
              type: string
              description: Tipo principal de pausa
              example: "CAPACITACION"
            subestado:
              type: string
              description: Subtipo de pausa (opcional)
              example: "INTERNA"
            observacion:
              type: string
              description: Detalle adicional
            fecha:
              type: string
              format: date
              description: Fecha de la pausa (YYYY-MM-DD)
            horaInicio:
              type: string
              description: Hora de inicio (HH:MM)
            horaFin:
              type: string
              description: Hora de fin (HH:MM, opcional si está en curso)
            usuario:
              type: string
              description: Usuario que registra la acción
              default: "ADMIN_API"
    responses:
      200:
        description: Pausas registradas exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "3 pausas registradas"
      400:
        description: Error de validación (ej. falta empleados)
      500:
        description: Error interno del servidor
    """
    try:
        data = request.json
        count = PauseService.create_pausas(data)
        return jsonify({"success": True, "message": f"{count} pausas registradas"})
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@pause_bp.route('/api/pausas/<int:id_pausa>', methods=['PUT'])
def update_pausa(id_pausa):
    """
    Actualizar una pausa existente
    Permite modificar observaciones o cerrar una pausa abierta (agregar hora fin).
    ---
    tags:
      - Pausas
    parameters:
      - name: id_pausa
        in: path
        type: integer
        required: true
        description: ID único del registro de pausa
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            observacion:
              type: string
            horaFin:
              type: string
              description: Nueva hora fin para cerrar la pausa
            usuario:
              type: string
              description: Usuario que realiza la modificación
    responses:
      200:
        description: Pausa actualizada correctamente
      404:
        description: Pausa no encontrada
      500:
        description: Error interno del servidor
    """
    try:
        data = request.json
        success = PauseService.update_pausa(id_pausa, data)
        if success:
            return jsonify({"success": True, "message": "Pausa actualizada"})
        return jsonify({"success": False, "message": "Pausa no encontrada"}), 404
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@pause_bp.route('/api/pausas/<int:id_pausa>', methods=['DELETE'])
def delete_pausa(id_pausa):
    """
    Eliminar una pausa
    Borra permanentemente un registro de pausa por su ID.
    ---
    tags:
      - Pausas
    parameters:
      - name: id_pausa
        in: path
        type: integer
        required: true
        description: ID de la pausa a eliminar
    responses:
      200:
        description: Pausa eliminada correctamente
      404:
        description: Pausa no encontrada
      500:
        description: Error interno del servidor
    """
    try:
        success = PauseService.delete_pausa(id_pausa)
        if success:
            return jsonify({"success": True, "message": "Pausa eliminada"})
        return jsonify({"success": False, "message": "Pausa no encontrada"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@pause_bp.route('/api/reportes/pausas-visitas', methods=['GET'])
def report_pausas_visitas():
    """
    Alias para obtener pausas
    Endpoint de compatibilidad que redirige a get_pausas.
    ---
    tags:
      - Reportes
    responses:
      200:
        description: Mismo resultado que GET /api/pausas
    """
    return get_pausas()
