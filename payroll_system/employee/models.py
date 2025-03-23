from django.db import models

class Employee(models.Model):
    """
    Model representing an Employee.

    This model stores the following details about an employee:
    - first_name: The employee's first name.
    - last_name: The employee's last name.
    - email: The employee's email address (unique).
    - hire_date: The date when the employee was hired.
    - position: The employee's job position.
    - status: The employment status, which can be either 'Active' or 'Inactive'.

    Methods:
        __str__: Returns the full name of the employee in the format "First Name Last Name".
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
        Returns a string representation of the Employee object, displaying the employee's full name.

        Example:
            "Leo Dellosa"
        """
        return f"{self.first_name} {self.last_name}"

