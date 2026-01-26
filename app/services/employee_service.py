from app.repositories.employee_repository import EmployeeRepository

class EmployeeService:
    @staticmethod
    def get_employees():
        employees = EmployeeRepository.get_all_active()
        return [emp.to_dict() for emp in employees]
