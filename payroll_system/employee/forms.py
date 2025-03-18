from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    """
    Form for creating and updating Employee records.

    This form is used to input the details of an employee, including:
    - first_name: The first name of the employee.
    - last_name: The last name of the employee.
    - email: The email address of the employee.
    - hire_date: The date when the employee was hired.
    - position: The employee's job position.

    The form will also validate the data to ensure that all necessary fields are filled.
    """
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'hire_date', 'position']
