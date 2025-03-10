from django.shortcuts import redirect, render
from .models import Employee, Payroll
from django.http import HttpResponse
from django.db.models import Sum 
from .forms import EmployeeForm

def employeeList(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

def dashboard(request):
    total_employees = Employee.objects.count()
    total_payroll = Payroll.objects.aggregate(Sum('net_salary'))['net_salary__sum']
    latest_payroll = Payroll.objects.order_by('-id').first()

    context = {
        'total_employees': total_employees,
        'total_payroll': total_payroll,
        'latest_payroll': latest_payroll,
    }
    return render(request, 'dashboard.html', context)

def addEmployee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        
        if form.is_valid():
            # Save the form data to the database
            form.save()

            # Redirect after saving
            return redirect('employee_list')  # Redirect to the employee list page or another page after adding the employee
        else:
            # If form is not valid, you can display errors (optional)
            return render(request, 'add_employee.html', {'form': form})
    else:
        # If GET request, just render an empty form
        form = EmployeeForm()
        return render(request, 'add_employee.html', {'form': form})