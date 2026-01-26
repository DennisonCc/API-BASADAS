from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# PostgreSQL Connection for Docker (using WSL IP for consistency)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://root:root@192.168.208.97:5435/personal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Endpoints del Módulo: Tiempos fuera de trabajo ---

@app.route('/')
def index():
    return render_template('index.html')

# 1. Obtener empleados activos (para llenar combos/listas)
@app.route('/api/empleados', methods=['GET'])
def get_empleados():
    try:
        with db.engine.connect() as conn:
            result = conn.execute(db.text("SELECT CI, NOMBRES, APELLIDOS FROM empleado")) 
            employees = []
            for row in result:
                employees.append({
                    "id": row.ci,
                    "name": f"{row.nombres} {row.apellidos}",
                    "role": "Empleado"
                })
            return jsonify(employees)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# 2. CRUD Pausas: Listar / Buscar con filtros (Equivalente al Reporte Java)
@app.route('/api/pausas', methods=['GET'])
def get_pausas():
    try:
        ci = request.args.get('ci', '%')
        fecha_inicio = request.args.get('fecha_inicio', '1900-01-01')
        fecha_fin = request.args.get('fecha_fin', '2100-12-31')
        
        query = db.text("""
            SELECT p.*, e.NOMBRES, e.APELLIDOS 
            FROM pausas p
            JOIN empleado e ON p.empleado_pausa = e.CI
            WHERE p.empleado_pausa LIKE :ci 
            AND p.fecha_pausa BETWEEN :f_inicio AND :f_fin
            ORDER BY p.fecha_pausa DESC, p.hora_inicio_pausa DESC
        """)
        
        with db.engine.connect() as conn:
            result = conn.execute(query, {"ci": ci, "f_inicio": fecha_inicio, "f_fin": fecha_fin})
            pausas = []
            for row in result:
                pausas.append({
                    "id": row.id_pausa,
                    "tipo": row.tipo_pausa,
                    "sub_tipo": row.sub_tipo_pausa,
                    "empleado_id": row.empleado_pausa,
                    "empleado_nombre": f"{row.nombres} {row.apellidos}",
                    "observacion": row.observacion_pausa,
                    "fecha": str(row.fecha_pausa),
                    "hora_inicio": row.hora_inicio_pausa,
                    "hora_fin": row.hora_fin_pausa,
                    "fecha_edicion": str(row.fecha_edicion),
                    "usuario_edicion": row.usuario_edicion
                })
            return jsonify(pausas)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# 3. CRUD Pausas: Insertar (Equivalente a PausasActivas.java)
@app.route('/api/pausas', methods=['POST'])
def create_pausas():
    data = request.json
    try:
        empleados = data.get('empleados', [])
        if not empleados:
            return jsonify({"success": False, "message": "Seleccione al menos un empleado"}), 400
            
        now = datetime.now()
        fecha_edicion = now.strftime("%Y-%m-%d %H:%M:%S")
        
        query = db.text("""
            INSERT INTO pausas 
            (tipo_pausa, sub_tipo_pausa, empleado_pausa, observacion_pausa, fecha_pausa, 
             hora_inicio_pausa, hora_fin_pausa, fecha_edicion, usuario_edicion)
            VALUES 
            (:tipo, :sub, :ci, :obs, :fecha, :h_i, :h_f, :f_edicion, :user)
        """)
        
        with db.engine.begin() as conn:
            for ci in empleados:
                conn.execute(query, {
                    "tipo": data.get('estado'),
                    "sub": data.get('subestado'),
                    "ci": ci,
                    "obs": data.get('observacion', ''),
                    "fecha": data.get('fecha'),
                    "h_i": data.get('horaInicio'),
                    "h_f": data.get('horaFin', ''),
                    "f_edicion": fecha_edicion,
                    "user": data.get('usuario', 'ADMIN_API')
                })
        return jsonify({"success": True, "message": f"{len(empleados)} pausas registradas"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# 4. CRUD Pausas: Actualizar (Equivalente a update_pausas en Java)
@app.route('/api/pausas/<int:id_pausa>', methods=['PUT'])
def update_pausa(id_pausa):
    data = request.json
    try:
        now = datetime.now()
        fecha_edicion = now.strftime("%Y-%m-%d %H:%M:%S")
        
        query = db.text("""
            UPDATE pausas 
            SET observacion_pausa = :obs, 
                hora_fin_pausa = :h_f, 
                fecha_edicion = :f_edicion, 
                usuario_edicion = :user
            WHERE id_pausa = :id
        """)
        
        with db.engine.begin() as conn:
            conn.execute(query, {
                "obs": data.get('observacion'),
                "h_f": data.get('horaFin'),
                "f_edicion": fecha_edicion,
                "user": data.get('usuario', 'ADMIN_API'),
                "id": id_pausa
            })
        return jsonify({"success": True, "message": "Pausa actualizada"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# 5. CRUD Pausas: Eliminar (Extra para completitud)
@app.route('/api/pausas/<int:id_pausa>', methods=['DELETE'])
def delete_pausa(id_pausa):
    try:
        query = db.text("DELETE FROM pausas WHERE id_pausa = :id")
        with db.engine.begin() as conn:
            conn.execute(query, {"id": id_pausa})
        return jsonify({"success": True, "message": "Pausa eliminada"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# 6. Reporte Específico (Equivalente a recuperar_pausas_visitas con filtros manuales)
@app.route('/api/reportes/pausas-visitas', methods=['GET'])
def report_pausas_visitas():
    # Es básicamente el mismo lógica que GET /api/pausas pero filtrado o con formato reporte
    return get_pausas()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
