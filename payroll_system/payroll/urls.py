from django.urls import path
from . import views

urlpatterns = [
    # Route to the dashboard view (home page for the app).
    # This will render the dashboard view, typically displaying an overview or stats.
    path('', views.dashboard, name='dashboard'),

    # Route to generate a payroll for an employee.
    # This will render the generatePayroll view to generate and possibly display payroll information.
    path('payroll/generate_payroll/', views.generatePayroll, name='generate_payroll'),

    # Route to view the payroll summary for all employees.
    # This will render the payrollSummary view to display a summary of payroll information
    path('payroll/payroll_summary/', views.payrollSummary, name='payroll_summary'),

    # Rounte to generate a payslip for an employee.
    # This will render the generatePaslipExcel view to generate and download a payslip in Excel format.
    path('generate_payslip_excel/<int:employee_id>/', views.generatePayslipExcel, name='generate_payslip_excel'),

    # Route to export a payslip for an employee in PDF format.
    # This will render the exportPayslipPdf view to generate and download a payslip in PDF format.
    path('export-payslip-pdf/<int:employee_id>/', views.exportPayslipPdf, name='export_payslip_pdf'),
]
