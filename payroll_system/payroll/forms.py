from django import forms
from .models import Employee, Payroll
from django.core.exceptions import ValidationError

class EmployeeForm(forms.ModelForm):
    """
    Form for creating and updating Employee records.

    This form is used to input the details of an employee, including:
    - first_name: The first name of the employee.
    - last_name: The last name of the employee.
    - email: The email address of the employee.
    - hire_date: The date when the employee was hired.
    - position: The employee's job position.
    """
    class Meta:
        model = Employee 
        fields = ['first_name', 'last_name', 'email', 'hire_date', 'position'] 

class PayrollForm(forms.Form):
    """
    Form for generating and validating payroll details for an employee.

    This form is used to input payroll information, including:
    - employee: The employee for whom the payroll is being generated.
    - gross_salary: The gross salary before any deductions.
    - deductions: The deductions from the gross salary (e.g., taxes, benefits).
    - pay_period: The pay period for the payroll (in YYYY-MM-DD format).
    """
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(), 
        required=True, widget=forms.Select(attrs={'class': 'form-control'})
    )
    gross_salary = forms.DecimalField(
        max_digits=10, 
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Gross Salary'})
    )
    deductions = forms.DecimalField(
        max_digits=10, 
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Deductions'})
    )

    pay_period = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Pay Period (YYYY-MM-DD)', 'type': 'date'})
    )

    def clean_gross_salary(self):
        """
        Custom validation for gross salary.

        Ensures that the gross salary is a positive number.

        Returns:
            decimal: The cleaned (validated) gross salary.

        Raises:
            ValidationError: If the gross salary is less than or equal to zero.
        """
        gross_salary = self.cleaned_data.get('gross_salary')
        if gross_salary <= 0:
            raise ValidationError("Gross salary must be greater than zero.")
        return gross_salary

    def clean_deductions(self):
        """
        Custom validation for deductions.

        Ensures that the deductions are not negative and do not exceed the gross salary.

        Returns:
            decimal: The cleaned (validated) deductions.

        Raises:
            ValidationError: If the deductions are less than zero or greater than the gross salary.
        """
        gross_salary = self.cleaned_data.get('gross_salary')
        deductions = self.cleaned_data.get('deductions')
        if deductions < 0:
            raise ValidationError("Deductions cannot be negative.")
        if deductions > gross_salary:
            raise ValidationError("Deductions cannot exceed the gross salary.")
        return deductions

    def clean(self):
        """
        Custom validation to ensure deductions do not exceed gross salary.

        This method is called after both individual field validations are done. It checks that
        the deductions do not exceed the gross salary and adds a 'net_salary' field to the cleaned data.

        Returns:
            dict: The cleaned and validated data, including the calculated net salary.

        Raises:
            ValidationError: If deductions exceed the gross salary.
        """
        cleaned_data = super().clean()
        gross_salary = cleaned_data.get('gross_salary')
        deductions = cleaned_data.get('deductions')

        if gross_salary and deductions:
            if deductions > gross_salary:
                raise ValidationError("Deductions cannot be greater than the gross salary.")
            # Calculate the net salary and add it to the cleaned data
            cleaned_data['net_salary'] = gross_salary - deductions

        return cleaned_data
