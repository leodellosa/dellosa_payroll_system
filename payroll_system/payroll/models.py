from django.db import models
from django.utils import timezone
from employee.models import Employee

class Payroll(models.Model):
    """
    Model representing the Payroll details of an Employee.

    This model stores payroll-related data for an employee for a specific period:
    - employee: The employee for whom the payroll record is created.
    - daily_rate: The employee's daily rate of pay.
    - allowance: Any allowances provided to the employee.
    - total_hours_worked: The total number of hours worked by the employee in the period.
    - overtime_pay: The pay for any overtime worked by the employee.
    - overtime_hour: The number of overtime hours worked.
    - night_differential_pay: The pay for night differential hours worked.
    - night_differential_hour: The number of night differential hours worked.
    - deductions: Any deductions made from the employee's salary.
    - deduction_remarks: Additional remarks related to the deductions.
    - subtotal: The subtotal salary before deductions.
    - net_salary: The final salary after deductions.
    - date: The date for the payroll record (e.g., pay period date).
    - time_in: The time the employee clocked in for the day.
    - time_out: The time the employee clocked out for the day.
    - project: An optional project associated with the employee's work.
    - created_at: The timestamp when the payroll record was created.

    Methods:
        __str__: Returns a string representation of the Payroll object, showing the employee and the date of the payroll.
    """

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    overtime_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overtime_hour = models.DecimalField(max_digits=10, decimal_places=2)
    night_differential_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    night_differential_hour = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deduction_remarks = models.CharField(max_length=200, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateField(default=timezone.now)
    time_in = models.DateTimeField()
    time_out = models.DateTimeField()
    project = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the Payroll object, showing the employee and the date of the payroll.

        Example:
            "Leo Dellosa - 2025-03-15"
        """
        return f'{self.employee} - {self.date}'
