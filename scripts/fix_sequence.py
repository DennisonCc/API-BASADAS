from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        print("Intentando corregir la secuencia de IDs en la tabla pausas...")
        # Postgres specific command to reset sequence to max(id) + 1
        sql = text("SELECT setval('pausas_id_pausa_seq', (SELECT MAX(id_pausa) FROM pausas) + 1);")
        result = db.session.execute(sql)
        db.session.commit()
        print(f"Secuencia actualizada exitosamente: {result}")
    except Exception as e:
        print(f"Error al actualizar secuencia: {e}")
