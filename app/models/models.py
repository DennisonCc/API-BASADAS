from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = 'empleado'
    ci = db.Column('ci', db.String(20), primary_key=True)
    nombres = db.Column('nombres', db.String(100))
    apellidos = db.Column('apellidos', db.String(100))

    def to_dict(self):
        return {
            "id": self.ci,
            "name": f"{self.nombres} {self.apellidos}",
            "role": "Empleado"
        }

class Pause(db.Model):
    __tablename__ = 'pausas'
    id_pausa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_pausa = db.Column(db.String(50))
    sub_tipo_pausa = db.Column(db.String(50))
    empleado_pausa = db.Column(db.String(20), db.ForeignKey('empleado.ci'))
    observacion_pausa = db.Column(db.Text)
    fecha_pausa = db.Column(db.Date)
    hora_inicio_pausa = db.Column(db.String(10))
    hora_fin_pausa = db.Column(db.String(10))
    fecha_edicion = db.Column(db.DateTime, default=datetime.now)
    usuario_edicion = db.Column(db.String(50))

    # Relationship
    employee = db.relationship('Employee', backref='pausas')

    def to_dict(self):
        return {
            "id": self.id_pausa,
            "tipo": self.tipo_pausa,
            "sub_tipo": self.sub_tipo_pausa,
            "empleado_id": self.empleado_pausa,
            "empleado_nombre": f"{self.employee.nombres} {self.employee.apellidos}" if self.employee else "Desconocido",
            "observacion": self.observacion_pausa,
            "fecha": str(self.fecha_pausa),
            "hora_inicio": self.hora_inicio_pausa,
            "hora_fin": self.hora_fin_pausa,
            "fecha_edicion": str(self.fecha_edicion),
            "usuario_edicion": self.usuario_edicion
        }
