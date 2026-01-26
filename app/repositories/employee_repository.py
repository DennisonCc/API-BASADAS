from app.models.models import Employee, db

class EmployeeRepository:
    @staticmethod
    def get_all_active():
        return Employee.query.all()

    @staticmethod
    def get_by_ci(ci):
        return Employee.query.get(ci)
