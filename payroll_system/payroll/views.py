from django.shortcuts import get_object_or_404, redirect, render
from .forms import EmployeeForm, PayrollForm
from .models import Employee, Payroll
from django.contrib import messages
from django.utils.dateparse import parse_datetime

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
    return redirect('employee_list')

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
    View to generate payroll for an employee.

    The form collects details such as time in, time out, total hours worked, deductions,
    overtime pay, and night differential pay. It computes the gross salary, net salary, 
    and the final payroll for the employee. The result is saved to the Payroll model.

    - POST method: Handles payroll generation and saves the data.
    - GET method: Displays an empty payroll form.
    """
    if request.method == 'POST':
        form = PayrollForm(request.POST)

        if form.is_valid():
            # Get the employee and payroll details from the form
            employee = form.cleaned_data['employee']
            time_in = form.cleaned_data['time_in']
            time_out = form.cleaned_data['time_out']

            if isinstance(time_in, str) and time_in:
                time_in = parse_datetime(time_in)
            if isinstance(time_out, str) and time_out:
                time_out = parse_datetime(time_out)

            total_hours_worked = form.cleaned_data['total_hours_worked']
            deductions = form.cleaned_data['deductions']
            subtotal = form.cleaned_data['subtotal']
            net_salary = form.cleaned_data['net_salary']
            deduction_remarks = form.cleaned_data['deduction_remarks']
            project = form.cleaned_data['project']
            daily_rate = form.cleaned_data['daily_rate']
            overtime_pay = form.cleaned_data['overtime_pay']
            overtime_hour = form.cleaned_data['overtime_hour']
            night_differential_pay = form.cleaned_data['night_differential_pay']
            night_differential_hour = form.cleaned_data['night_differential_hour']
            allowance = form.cleaned_data['allowance']
            
            # Creating a Payroll instance and saving it to the database
            payroll = Payroll(
                employee=employee,
                time_in=time_in,
                time_out=time_out,
                total_hours_worked=total_hours_worked,
                deductions=deductions,
                subtotal=subtotal,
                net_salary=net_salary,
                deduction_remarks=deduction_remarks,
                project=project,
                daily_rate=daily_rate,
                overtime_pay = overtime_pay,
                overtime_hour = overtime_hour,
                night_differential_pay = night_differential_pay,
                night_differential_hour = night_differential_hour,  
                allowance = allowance
            )
            print("valid",payroll)
            payroll.save()

            # Notify the user that the payroll was successfully generated
            messages.success(request, f"Payroll for {employee} has been successfully generated!")

            # Redirect to another page, such as a summary of generated payroll
            return redirect('payroll_summary')  # You can replace with the correct URL name or path

        else:
            # If the form is not valid, display errors
            for field in form:
                for error in field.errors:
                    messages.error(request, f"Error in {field.label}: {error}")
            return render(request, 'generate_payroll.html', {
                'form': form,
                'total_hours_worked': form.cleaned_data.get('total_hours_worked', 0),
            })

    else:
        form = PayrollForm()
        return render(request, 'generate_payroll.html', {'form': form})



from django.shortcuts import render, get_object_or_404
from .models import Employee, Payroll

def payrollSummary(request):
    """
    View to display the payroll summary for all employees or a specific employee.

    This view displays a list of generated payrolls, with the option to filter by employee.
    The summary will show the payroll details such as the employee's name, pay period, 
    gross salary, deductions, and net salary.
    """
    employees = Employee.objects.all()

    # Default to show payroll summary for all employees
    selected_employee = None
    payrolls = Payroll.objects.all()

    # Check if the form was submitted with a GET request
    if request.method == 'GET':
        selected_employee_id = request.GET.get('employee')
        if selected_employee_id:
            selected_employee = get_object_or_404(Employee, id=selected_employee_id)
            payrolls = Payroll.objects.filter(employee=selected_employee)

        # Calculate totals for the selected employee's payrolls
        total_hours_worked = sum(payroll.total_hours_worked for payroll in payrolls)
        total_overtime_pay = sum(payroll.overtime_pay for payroll in payrolls)
        total_night_differential_pay = sum(payroll.night_differential_pay for payroll in payrolls)
        allowance = sum(payroll.allowance for payroll in payrolls)
        total_deductions = sum(payroll.deductions for payroll in payrolls)
        total_gross_salary = sum(payroll.subtotal for payroll in payrolls)
        total_net_salary = sum(payroll.net_salary for payroll in payrolls)

        return render(request, 'payroll_summary.html', {
            'payrolls': payrolls,
            'employees': employees,
            'selected_employee': selected_employee,
            'total_hours_worked': total_hours_worked,
            'total_overtime_pay': total_overtime_pay,
            'total_night_differential_pay': total_night_differential_pay,
            'allowance': allowance,
            'total_deductions': total_deductions,
            'total_gross_salary': total_gross_salary,
            'total_net_salary': total_net_salary
        })
