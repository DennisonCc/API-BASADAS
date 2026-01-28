from app.repositories.pause_repository import PauseRepository
from app.repositories.employee_repository import EmployeeRepository
from datetime import datetime

class PauseService:
    @staticmethod
    def _validate_overlap(ci, fecha, hora_inicio, hora_fin):
        existing_pauses = PauseRepository.get_by_employee_date(ci, fecha)
        new_start = datetime.strptime(hora_inicio, '%H:%M')
        new_end = datetime.strptime(hora_fin, '%H:%M') if hora_fin else None
        
        for p in existing_pauses:
            if not p.hora_inicio_pausa: continue
            
            ex_start = datetime.strptime(p.hora_inicio_pausa, '%H:%M')
            ex_end = datetime.strptime(p.hora_fin_pausa, '%H:%M') if p.hora_fin_pausa else None

            # Si hay una pausa abierta existente, choca con cualquier nueva pausa
            # a menos que la nueva termine antes de que empiece la existente (improbable usuario input)
            if ex_end is None:
                if new_end and new_end <= ex_start:
                    continue
                return True

            # Si la nueva es abierta check si empieza antes de que termine una cerrada
            if new_end is None:
                if new_start < ex_end:
                    return True
            
            # Ambas cerradas: chequeo estandar
            else:
                if new_start < ex_end and new_end > ex_start:
                    return True
        return False

    @staticmethod
    def get_pausas(ci=None, fecha_inicio=None, fecha_fin=None):
        pausas = PauseRepository.get_filtered(ci, fecha_inicio, fecha_fin)
        return [p.to_dict() for p in pausas]

    @staticmethod
    def create_pausas(data):
        # 1. Validar campos requeridos
        required_fields = ['empleados', 'estado', 'fecha', 'horaInicio']
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"El campo '{field}' es obligatorio")

        empleados = data.get('empleados', [])
        if not isinstance(empleados, list) or not empleados:
             raise ValueError("Debe seleccionar al menos un empleado")

        start_time = data.get('horaInicio')

        end_time = data.get('horaFin')
        date_str = data.get('fecha')

        # 2. Validar formato de fecha y hora
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            datetime.strptime(start_time, '%H:%M')
            if end_time:
                datetime.strptime(end_time, '%H:%M')
        except ValueError:
            raise ValueError("Formato de fecha (YYYY-MM-DD) u hora (HH:MM) inválido")

        # 3. Validar coherencia de horas
        if end_time and end_time <= start_time:
            raise ValueError("La hora de fin debe ser posterior a la hora de inicio")

        for ci in empleados:
            # 4. Validar existencia del empleado
            employee = EmployeeRepository.get_by_ci(ci)
            if not employee:
                raise ValueError(f"El empleado con CI {ci} no existe en la base de datos")

            # 5. Validar solapamiento de pausas
            # Pasamos date_obj (objeto date) en lugar de string para comparaciones correctas si fuera necesario, 
            # aunque _validate_overlap usa el repositorio que espera convertirlo, pero
            # para consistencia usemos el string en el filtro del repo o el objeto.
            # Nota: El repo PauseRepository.get_by_employee_date espera 'fecha'.
            # Si SQLalchemy en SQLite falla con string, es mejor pasar date_obj al repo.
            if PauseService._validate_overlap(ci, date_obj, start_time, end_time):
                raise ValueError(f"El empleado {employee.nombres} {employee.apellidos} ya tiene una pausa en conflictos con el horario {start_time}-{end_time}")

            PauseRepository.create({
                "tipo": data.get('estado'),
                "sub_tipo": data.get('subestado'),
                "empleado_id": ci,
                "observacion": data.get('observacion', ''),
                "fecha": date_obj, # Enviamos el objeto date, no el string
                "hora_inicio": start_time,
                "hora_fin": end_time if end_time else '',
                "usuario": data.get('usuario', 'ADMIN_API')
            })
        
        PauseRepository.commit()
        return len(empleados)

    @staticmethod
    def update_pausa(id_pausa, data):
        pause = PauseRepository.get_by_id(id_pausa)
        if not pause:
            return False

        if 'horaFin' in data and data['horaFin']:
            try:
                end_time = datetime.strptime(data['horaFin'], '%H:%M')
                start_time = datetime.strptime(pause.hora_inicio_pausa, '%H:%M')
                if end_time <= start_time:
                    raise ValueError("La hora de fin debe ser posterior a la de inicio")
            except ValueError as e:
                if "posterior" in str(e): raise e
                raise ValueError("Formato de hora fin inválido (HH:MM)")

        updated_pause = PauseRepository.update(id_pausa, {
            "observacion": data.get('observacion'),
            "hora_fin": data.get('horaFin'),
            "usuario": data.get('usuario', 'ADMIN_API')
        })
        
        if updated_pause:
            PauseRepository.commit()
            return True
        return False

    @staticmethod
    def delete_pausa(id_pausa):
        success = PauseRepository.delete(id_pausa)
        if success:
            PauseRepository.commit()
        return success
