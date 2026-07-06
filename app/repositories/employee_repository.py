from app.models import Employee

from .base_repository import BaseRepository


class EmployeeRepository(BaseRepository):
    model = Employee

    def get_by_email(self, email):
        return Employee.query.filter(Employee.email == email).first()

    def get_by_id_card_no(self, id_card_no):
        return Employee.query.filter(Employee.id_card_no == id_card_no).first()

    def get_duplicate_value(self, field_name, value, exclude_employee_id=None):
        query = Employee.query.filter(getattr(Employee, field_name) == value)
        if exclude_employee_id:
            query = query.filter(Employee.id != exclude_employee_id)
        return query.first()

    def list_by_organisation_id(self, organisation_id):
        return (
            Employee.query.filter(Employee.organisation_id == organisation_id)
            .order_by(Employee.id)
            .all()
        )
