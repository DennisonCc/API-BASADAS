from app.models.models import Pause, db
from datetime import datetime

class PauseRepository:
    @staticmethod
    def get_filtered(ci=None, fecha_inicio=None, fecha_fin=None):
        query = Pause.query
        if ci and ci != '%':
            query = query.filter(Pause.empleado_pausa == ci)
        if fecha_inicio:
            query = query.filter(Pause.fecha_pausa >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Pause.fecha_pausa <= fecha_fin)
        
        return query.order_by(Pause.fecha_pausa.desc(), Pause.hora_inicio_pausa.desc()).all()

    @staticmethod
    def get_by_employee_date(ci, fecha):
        return Pause.query.filter(Pause.empleado_pausa == ci, Pause.fecha_pausa == fecha).all()

    @staticmethod
    def get_by_id(id_pausa):
        return Pause.query.get(id_pausa)

    @staticmethod
    def create(data):
        pause = Pause(
            tipo_pausa=data.get('tipo'),
            sub_tipo_pausa=data.get('sub_tipo'),
            empleado_pausa=data.get('empleado_id'),
            observacion_pausa=data.get('observacion'),
            fecha_pausa=data.get('fecha'),
            hora_inicio_pausa=data.get('hora_inicio'),
            hora_fin_pausa=data.get('hora_fin'),
            usuario_edicion=data.get('usuario', 'ADMIN_API'),
            fecha_edicion=datetime.now()
        )
        db.session.add(pause)
        return pause

    @staticmethod
    def update(id_pausa, data):
        pause = Pause.query.get(id_pausa)
        if pause:
            pause.observacion_pausa = data.get('observacion', pause.observacion_pausa)
            pause.hora_fin_pausa = data.get('hora_fin', pause.hora_fin_pausa)
            pause.usuario_edicion = data.get('usuario', pause.usuario_edicion)
            pause.fecha_edicion = datetime.now()
        return pause

    @staticmethod
    def delete(id_pausa):
        pause = Pause.query.get(id_pausa)
        if pause:
            db.session.delete(pause)
            return True
        return False

    @staticmethod
    def commit():
        db.session.commit()
