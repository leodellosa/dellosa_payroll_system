from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee  # Specify the model that this form is associated with
        fields = ['first_name','last_name','email','hire_date', 'position']  # Fields from the Employee model
        
