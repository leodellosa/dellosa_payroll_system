from django.shortcuts import get_object_or_404, redirect, render
from .forms import EmployeeForm, PayrollForm
from .models import Employee, Payroll
from django.contrib import messages
from django.utils import timezone

def employeeList(request):
    """
    View to display a list of all employees.

    Retrieves all employee records from the database and passes them
    to the 'employee_list.html' template for rendering.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the employee_list.html template with all employees.
    """
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

def dashboard(request):
    """
    View to display the dashboard page.

    Retrieves statistics such as the total number of employees and other
    dashboard-related data (currently commented-out) to pass to the template.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the dashboard.html template with employee statistics.
    """
    total_employees = Employee.objects.count()
    context = {
        'total_employees': total_employees,
    }
    return render(request, 'dashboard.html', context)

def addEmployee(request):
    """
    View to handle the addition of a new employee.

    Displays a form to create a new employee and saves the employee's data
    to the database if the form is valid. On successful creation, redirects
    to the employee list page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the 'add_employee.html' template with the form,
        or redirects to the employee list if the form is valid.
    """
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('employee_list')
        else:
            return render(request, 'add_employee.html', {'form': form})
    else:
        form = EmployeeForm()
        return render(request, 'add_employee.html', {'form': form})

def employeeDetails(request, employee_id):
    """
    View to display details of a specific employee.

    Retrieves a specific employee based on the given employee_id and renders
    the 'employee_detail.html' template with the employee's information.

    Args:
        request: The HTTP request object.
        employee_id: The ID of the employee to be displayed.

    Returns:
        HttpResponse: Renders the 'employee_detail.html' template with the
        employee details.
    """
    employee = get_object_or_404(Employee, id=employee_id)
    return render(request, 'employee_detail.html', {'employee': employee})

def editEmployee(request, employee_id):
    """
    View to edit an existing employee's details.

    Retrieves the employee based on the given employee_id and displays a
    form pre-filled with the employee's current details. On successful form
    submission, updates the employee's details in the database.

    Args:
        request: The HTTP request object.
        employee_id: The ID of the employee to be edited.

    Returns:
        HttpResponse: Renders the 'edit_employee.html' template with the form
        for editing the employee details, or redirects to the employee details
        page if the form is valid.
    """
    employee = get_object_or_404(Employee, id=employee_id)

    # Capture the referrer URL
    referer = request.META.get('HTTP_REFERER', '/')

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_details', employee_id=employee.id)
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'edit_employee.html', {
        'form': form,
        'employee': employee,
        'referer': referer
    })

def updateEmployeeStatus(request, employee_id):
    """
    View to update the employment status of a specific employee.

    Retrieves the employee based on the given employee_id and toggles their
    status between 'Active' and 'Inactive'. The updated status is saved in the database.

    Args:
        request: The HTTP request object.
        employee_id: The ID of the employee whose status needs to be updated.

    Returns:
        HttpResponse: Redirects to the employee list after the status update.
    """
    employee = get_object_or_404(Employee, id=employee_id)
    
    if employee.status == 'Active':
        employee.status = 'Inactive'
    else:
        employee.status = 'Active'
    
    employee.save()

    return redirect('employee_list')

def generatePayroll(request):
    """
    View to generate a payroll record for an employee.

    Displays a form for creating payroll entries, validates the form input,
    and creates a payroll record in the database upon successful submission.
    Displays success or error messages based on form validation results.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the 'generate_payroll.html' template with the form,
        or redirects to the same page if payroll is successfully created.
    """
    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            employee = form.cleaned_data['employee']
            gross_salary = form.cleaned_data['gross_salary']
            deductions = form.cleaned_data['deductions']
            pay_period = form.cleaned_data['pay_period']
            net_salary = form.cleaned_data['net_salary'] 

            # Create the payroll record
            payroll = Payroll.objects.create(
                employee=employee,
                gross_salary=gross_salary,
                deductions=deductions,
                net_salary=net_salary,
                pay_period=pay_period,
                created_at=timezone.now()
            )

            payroll.save()
            messages.success(request, "Payroll generated successfully!")
            return redirect('generate_payroll') 
        else:
            # Add error messages for the form fields that failed validation
            for field in form:
                for error in field.errors:
                    messages.error(request, f"Error in {field.label}: {error}")
    else:
        form = PayrollForm()
        form.fields['employee'].queryset = Employee.objects.all()

    return render(request, 'generate_payroll.html', {'form': form})
