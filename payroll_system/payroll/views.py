from django.shortcuts import get_object_or_404, redirect, render
from .forms import PayrollForm
from .models import Payroll
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from employee.models import Employee
from django.http import HttpResponse
from django.template.loader import render_to_string
# from weasyprint import HTML
from openpyxl import Workbook
from django.db.models import Sum


def dashboard(request):
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

        # Pass the data to the template
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


# def generatePayslip(request, payroll_id):
#     payroll = Payroll.objects.get(id=payroll_id)
#     html_string = render_to_string('payroll_payslip.html', {'payroll': payroll})
#     pdf = HTML(string=html_string).write_pdf()

#     # Add success message to Django messages framework
#     messages.success(request, 'Payroll summary has been successfully generated.')

#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="payslip_{payroll.employee.first_name}_{payroll.employee.last_name}_{payroll.date}.pdf"'
#     return response


def generatePayslipExcel(request, employee_id):
    """
    Generate and return an Excel payslip for a specific employee.

    This view fetches payroll records for the given employee and generates 
    an Excel file containing a summary of the employee's payroll information.
    The Excel file includes details such as the date, daily rate, allowance, 
    overtime pay, night differential pay, deductions, subtotal (gross salary), 
    and net salary. The file is then returned as a downloadable response.

    Parameters:
    request (HttpRequest): The HTTP request object containing user data and session information.
    employee_id (int): The ID of the employee for whom the payslip is being generated.

    Returns:
    HttpResponse: An HTTP response containing the generated Excel file as an attachment.

    Raises:
    Http404: If the employee with the given employee_id does not exist.
    
    Example:
    To generate a payslip for an employee with ID 1:
    GET /payroll/generate_payslip_excel/1/

    The resulting file will be an Excel document containing payroll details 
    for the specified employee.
    """
    employee = get_object_or_404(Employee, id=employee_id)
    payrolls = Payroll.objects.filter(employee=employee).select_related('employee').iterator(chunk_size=100)

    wb = Workbook()
    ws = wb.active
    ws.title = "Payslip"

    headers = [
        "Date","Time In","Time Out","Total Hours Worked", "Daily Rate","Overtime Hour", "Overtime Pay", 
        "Night Differential Hour","Night Differential Pay","Allowance", "Deductions","Deduction Remarks", "Subtotal", "Net Salary"
    ]
    ws.append(headers)

    batch = []

    for payroll in payrolls:
        data = [
            payroll.date.strftime("%Y-%m-%d"),
            payroll.time_in.strftime("%H:%M:%S"),
            payroll.time_out.strftime("%H:%M:%S"),
            payroll.total_hours_worked,
            payroll.daily_rate,
            payroll.overtime_hour,
            payroll.overtime_pay,
            payroll.night_differential_hour,
            payroll.night_differential_pay,
            payroll.allowance,
            payroll.deductions,
            payroll.deduction_remarks,
            payroll.subtotal,
            payroll.net_salary
        ]
        batch.append(data)

        # If the batch reaches a size, insert it into the worksheet
        if len(batch) >= 100:
            for row in batch:
                ws.append(row)
            batch.clear()  # Clear the batch

    # Add any remaining rows in the batch
    if batch:
        for row in batch:
            ws.append(row)

    messages.success(request, 'Payroll summary has been successfully generated.')

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="payslip_{employee.first_name}_{employee.last_name}.xlsx"'

    wb.save(response)

    return redirect('payroll_summary')



