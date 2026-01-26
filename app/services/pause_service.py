from app.repositories.pause_repository import PauseRepository

class PauseService:
    @staticmethod
    def get_pausas(ci=None, fecha_inicio=None, fecha_fin=None):
        pausas = PauseRepository.get_filtered(ci, fecha_inicio, fecha_fin)
        return [p.to_dict() for p in pausas]

    @staticmethod
    def create_pausas(data):
        empleados = data.get('empleados', [])
        if not empleados:
            raise ValueError("Seleccione al menos un empleado")
        
        for ci in empleados:
            PauseRepository.create({
                "tipo": data.get('estado'),
                "sub_tipo": data.get('subestado'),
                "empleado_id": ci,
                "observacion": data.get('observacion', ''),
                "fecha": data.get('fecha'),
                "hora_inicio": data.get('horaInicio'),
                "hora_fin": data.get('horaFin', ''),
                "usuario": data.get('usuario', 'ADMIN_API')
            })
        PauseRepository.commit()
        return len(empleados)

    @staticmethod
    def update_pausa(id_pausa, data):
        pause = PauseRepository.update(id_pausa, {
            "observacion": data.get('observacion'),
            "hora_fin": data.get('horaFin'),
            "usuario": data.get('usuario', 'ADMIN_API')
        })
        if pause:
            PauseRepository.commit()
            return True
        return False

    @staticmethod
    def delete_pausa(id_pausa):
        success = PauseRepository.delete(id_pausa)
        if success:
            PauseRepository.commit()
        return success
