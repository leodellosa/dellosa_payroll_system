from django.shortcuts import get_object_or_404, redirect, render
from .forms import PayrollForm
from .models import Payroll
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from employee.models import Employee
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from openpyxl import Workbook
from django.contrib.staticfiles import finders
from django.db.models import Min, Max
from django.utils import timezone
from openpyxl.drawing.image import Image
from openpyxl.styles import Alignment, Font

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
            form = PayrollForm()
            return render(request,'generate_payroll.html', {'form': form})  # You can replace with the correct URL name or path

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
    selected_employee = None
    payrolls = Payroll.objects.all()

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

def exportPayslipPdf(request, employee_id):
    """
    Generate and return a PDF payslip for a specific employee, including the company logo,
    name, position, pay period, date generated, daily rate, and summary.
    """
    employee = get_object_or_404(Employee, id=employee_id)
    payrolls = Payroll.objects.filter(employee=employee)

    if not payrolls:
        return HttpResponse("No payroll records found for this employee.", status=404)

    total_hours_worked = sum(payroll.total_hours_worked for payroll in payrolls)
    total_overtime_pay = sum(payroll.overtime_pay for payroll in payrolls)
    total_night_differential_pay = sum(payroll.night_differential_pay for payroll in payrolls)
    allowance = sum(payroll.allowance for payroll in payrolls)
    total_deductions = sum(payroll.deductions for payroll in payrolls)
    total_gross_salary = sum(payroll.subtotal for payroll in payrolls)
    total_net_salary = sum(payroll.net_salary for payroll in payrolls)
    pay_period_from = payrolls.aggregate(Min('date'))['date__min']
    pay_period_to = payrolls.aggregate(Max('date'))['date__max']
    current_date = timezone.now()
    daily_rate = payrolls.first().daily_rate

    html_string = render_to_string('payroll_payslip.html', {
        'selected_employee': employee,
        'payrolls': payrolls,
        'total_hours_worked': total_hours_worked,
        'total_overtime_pay': total_overtime_pay,
        'total_night_differential_pay': total_night_differential_pay,
        'allowance': allowance,
        'total_deductions': total_deductions,
        'total_gross_salary': total_gross_salary,
        'total_net_salary': total_net_salary,
        'pay_period_from': pay_period_from,
        'pay_period_to': pay_period_to,
        'current_date': current_date,
        'daily_rate': daily_rate
    })

    css_path = finders.find('css/payslip.css')

    if not css_path:
        return HttpResponse("CSS file not found.", status=404)

    # Pass the CSS path to WeasyPrint
    pdf_file = HTML(string=html_string,base_url=request.build_absolute_uri()).write_pdf(stylesheets=[css_path])

    # Return the PDF as a response
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="payslip_{employee.first_name}_{employee.last_name}.pdf"'
    return response


def generatePayslipExcel(request, employee_id):
    """
    Generate and return an Excel payslip for a specific employee, including the company logo, 
    name, position, pay period, date generated, daily rate, and summary.
    """
    employee = get_object_or_404(Employee, id=employee_id)
    payrolls = Payroll.objects.filter(employee=employee).select_related('employee')

    if not payrolls:
        return HttpResponse("No payroll records found for this employee.", status=404)

    wb = Workbook()
    ws = wb.active
    ws.title = "Payslip"

    logo_path = finders.find('img/company_logo.png')
    if logo_path:
        img = Image(logo_path)
        img.width = 120
        img.height = 80
        ws.add_image(img, 'A1')
    
    ws.merge_cells('C1:G1')
    ws['C1'] = "HODREAL FIT-OUT AND CONSTRUCTION"
    ws['C1'].alignment = Alignment(horizontal='left', vertical='center')
    ws['C1'].font = Font(bold=True, size=14)
    
    ws.merge_cells('C2:J2')
    ws['C2'] = "Bantangas City | Contact: 09217292222 | Email: hodrealconstruction@yahoo.com"
    ws['C2'].alignment = Alignment(horizontal='left', vertical='center')
    ws['C2'].font = Font(size=10)

    row_offset = 5 

    ws.merge_cells(f'A{row_offset}:F{row_offset}')
    ws[f'A{row_offset}'] = f"Employee: {employee.first_name} {employee.last_name}"
    ws[f'A{row_offset}'].font = Font(bold=True)
    ws[f'A{row_offset}'].alignment = Alignment(horizontal='left')

    ws.merge_cells(f'A{row_offset + 1}:F{row_offset + 1}')
    ws[f'A{row_offset + 1}'] = f"Position: {employee.position}"
    ws[f'A{row_offset + 1}'].font = Font(bold=True)
    ws[f'A{row_offset + 1}'].alignment = Alignment(horizontal='left')

    pay_period_from = payrolls.aggregate(Min('date'))['date__min']
    pay_period_to = payrolls.aggregate(Max('date'))['date__max']

    ws.merge_cells(f'A{row_offset + 2}:F{row_offset + 2}')
    ws[f'A{row_offset + 2}'] = f"Pay Period: {pay_period_from.strftime('%Y-%m-%d')} - {pay_period_to.strftime('%Y-%m-%d')}"
    ws[f'A{row_offset + 2}'].font = Font(bold=True)
    ws[f'A{row_offset + 2}'].alignment = Alignment(horizontal='left')

    ws.merge_cells(f'A{row_offset + 3}:F{row_offset + 3}')
    ws[f'A{row_offset + 3}'] = f"Date Generated: {timezone.now().strftime('%Y-%m-%d')}"
    ws[f'A{row_offset + 3}'].font = Font(bold=True)
    ws[f'A{row_offset + 3}'].alignment = Alignment(horizontal='left')

    daily_rate = payrolls.first().daily_rate
    ws.merge_cells(f'A{row_offset + 4}:F{row_offset + 4}')
    ws[f'A{row_offset + 4}'] = f"Daily Rate: {daily_rate}"
    ws[f'A{row_offset + 4}'].font = Font(bold=True)
    ws[f'A{row_offset + 4}'].alignment = Alignment(horizontal='left')

    row_offset += 7

    headers = [
        "Date", "Overtime", "Night Differential", "Allowance", "Deductions", "Total Amount"
    ]
    for col_num, header in enumerate(headers, 1):
        ws.cell(row=row_offset, column=col_num, value=header)
    
    for payroll in payrolls:
        ws.append([
            payroll.date.strftime("%Y-%m-%d"),
            payroll.overtime_pay,
            payroll.night_differential_pay,
            payroll.allowance,
            payroll.deductions,
            payroll.net_salary
        ])

    total_hours_worked = sum(payroll.total_hours_worked for payroll in payrolls)
    total_overtime_pay = sum(payroll.overtime_pay for payroll in payrolls)
    total_night_differential_pay = sum(payroll.night_differential_pay for payroll in payrolls)
    total_allowance = sum(payroll.allowance for payroll in payrolls)
    total_deductions = sum(payroll.deductions for payroll in payrolls)
    total_gross_salary = sum(payroll.subtotal for payroll in payrolls)
    total_net_salary = sum(payroll.net_salary for payroll in payrolls)

    row_offset += len(payrolls) + 3 

    ws[f'A{row_offset}'] = f"Total Hours Worked: {total_hours_worked}"
    ws[f'A{row_offset + 1}'] = f"Total Overtime Pay: {total_overtime_pay}"
    ws[f'A{row_offset + 2}'] = f"Total Night Differential Pay: {total_night_differential_pay}"
    ws[f'A{row_offset + 3}'] = f"Total Allowance: {total_allowance}"
    ws[f'A{row_offset + 4}'] = f"Total Deductions: {total_deductions}"
    ws[f'A{row_offset + 5}'] = f"Total Gross Salary: {total_gross_salary}"
    ws[f'A{row_offset + 6}'] = f"Total Net Salary: {total_net_salary}"

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="payslip_{employee.first_name}_{employee.last_name}.xlsx"'

    wb.save(response)
    return response
