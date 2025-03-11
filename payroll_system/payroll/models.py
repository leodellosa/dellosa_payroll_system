from django.db import models

class Employee(models.Model):
    """
    Model representing an Employee.

    This model is used to store employee-related information such as:
    - first_name: The employee's first name.
    - last_name: The employee's last name.
    - email: The employee's unique email address.
    - hire_date: The date when the employee was hired.
    - position: The employee's job position within the company.
    - status: The employment status of the employee (Active or Inactive).
    
    The `status` field is a choice field with two possible values: 'Active' and 'Inactive'.
    By default, a new employee will have a status of 'Active'.

    Methods:
        __str__: Returns a string representation of the employee, showing their full name.
    """
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    hire_date = models.DateField()
    position = models.CharField(max_length=100)

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Active',
    )

    def __str__(self):
        """
        String representation of the Employee object.

        Returns:
            str: The full name of the employee.
        """
        return f"{self.first_name} {self.last_name}"
    

class Payroll(models.Model):
    """
    Model representing Payroll information for an employee.

    This model is used to store payroll details such as:
    - employee: The Employee related to the payroll record (ForeignKey to Employee model).
    - gross_salary: The total salary before deductions.
    - deductions: The deductions applied to the gross salary (e.g., taxes, benefits).
    - net_salary: The final salary after deductions (gross salary - deductions).
    - pay_period: The pay period for which the payroll applies (e.g., 'January 2025').
    - created_at: The timestamp when the payroll record was created.

    Methods:
        __str__: Returns a string representation of the payroll, showing the employee and the net salary.
    """
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    pay_period = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        """
        String representation of the Payroll object.

        Returns:
            str: A string representing the employee and their net salary.
        """
        return f'{self.employee} - {self.net_salary}'
