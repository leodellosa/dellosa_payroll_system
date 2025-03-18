from decimal import Decimal
from django import forms
from .models import Payroll
from django.core.exceptions import ValidationError
from employee.models import Employee

class PayrollForm(forms.ModelForm):
    """
    Form for creating and updating Payroll records.

    This form handles the payroll processing for an employee, including:
    - employee: The employee receiving the payroll.
    - time_in: The time the employee started working on a particular day.
    - time_out: The time the employee finished working on that day.
    - total_hours_worked: The total number of hours worked by the employee on that day.
    - overtime_pay: The pay received for overtime worked.
    - overtime_hour: The number of overtime hours worked.
    - deductions: The total deductions for the employee.
    - subtotal: The subtotal salary before deductions.
    - net_salary: The final salary after deductions.
    - deduction_remarks: Any additional remarks related to the deductions.
    - project: Optional project details for the employee's work.
    - allowance: Any additional allowance added to the employee's pay.
    - night_differential_hour: Number of night differential hours worked.
    - night_differential_pay: The pay corresponding to the night differential hours worked.

    The form performs validation to ensure that:
    - Overtime cannot be recorded if total hours worked is less than 10.
    - Total hours worked must be greater than zero.
    - Deductions cannot exceed the gross salary.
    """
    
    class Meta:
        model = Payroll
        fields = [
            'employee', 'time_in', 'daily_rate', 'time_out', 'total_hours_worked', 'overtime_pay', 
            'overtime_hour', 'deductions', 'subtotal', 'net_salary', 'deduction_remarks', 
            'project', 'allowance', 'night_differential_pay', 'night_differential_hour'
        ]

    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    daily_rate = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Daily Rate'})
    )

    time_in = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )

    time_out = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )

    overtime_hour = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Overtime Hour'})
    )

    night_differential_hour = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Night Differential Hour'})
    )

    night_differential_pay = forms.DecimalField(
        required=False,
    )

    overtime_pay = forms.DecimalField(
        required=False,
    )

    subtotal = forms.DecimalField(
        required=False,
    )

    net_salary = forms.DecimalField(
        required=False,
    )

    allowance = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Allowance'})
    )

    deductions = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Deductions'})
    )

    deduction_remarks = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Deduction Remarks', 'rows': 3})
    )

    project = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project (Optional)'})
    )

    def clean(self):
        """
        Custom form validation to ensure the following:
        - Overtime hours cannot be recorded if total hours worked is less than 10.
        - Total hours worked must be greater than zero.
        - Deductions cannot exceed gross salary.
        
        Returns:
            cleaned_data: A dictionary containing cleaned data from the form.
        """
        cleaned_data = super().clean()
        total_hours_worked = cleaned_data.get('total_hours_worked')
        deductions = cleaned_data.get('deductions')
    
        overtime_hour = cleaned_data.get('overtime_hour', '')
        night_differential_hour = cleaned_data.get('night_differential_hour', '')
        allowance = cleaned_data.get('allowance', '')

        overtime_hour = Decimal(overtime_hour) if overtime_hour else Decimal(0)
        night_differential_hour = Decimal(night_differential_hour) if night_differential_hour else Decimal(0)
        deductions = Decimal(deductions) if deductions else Decimal(0)
        allowance = Decimal(allowance) if allowance else Decimal(0)

        # Check for overtime error
        if total_hours_worked is not None and overtime_hour > 0 and total_hours_worked < 10:
            raise ValidationError("Overtime cannot be recorded if total hours worked is less than 10.")

        # Check for total hours worked error
        if total_hours_worked is not None and total_hours_worked <= 0:
            raise ValidationError("Total hours worked cannot be less than or equal to zero.")
        
        # Calculate gross salary and net salary
        gross_salary = cleaned_data.get('subtotal')
        net_salary = gross_salary - deductions if gross_salary is not None else 0

        # Ensure deductions do not exceed gross salary
        if gross_salary and deductions > gross_salary:
            raise ValidationError("Deductions cannot exceed the gross salary.")

        cleaned_data['net_salary'] = net_salary
        cleaned_data['overtime_hour'] = overtime_hour
        cleaned_data['deductions'] = deductions
        cleaned_data['allowance'] = allowance
        cleaned_data['night_differential_hour'] = night_differential_hour
        return cleaned_data
