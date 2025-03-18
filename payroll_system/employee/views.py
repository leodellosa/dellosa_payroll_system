from django.shortcuts import get_object_or_404, redirect, render
from .forms import EmployeeForm
from .models import Employee

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
        # print(request.POST)
        form = EmployeeForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('employee_list')
        else:
            # print(form.errors)
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
    return render(request, 'employee_details.html', {'employee': employee})

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
