from django.urls import path
from . import views

urlpatterns = [
    # Route to the dashboard view (home page for the app).
    # This will render the dashboard view, typically displaying an overview or stats.
    path('', views.dashboard, name='dashboard'),

    # Route to the list of all employees.
    # This will render the employeeList view to display a list of employees.
    path('employees/', views.employeeList, name='employee_list'),

    # Route to view the details of a specific employee.
    # The employee_id is passed in the URL to identify the employee.
    path('employee/<int:employee_id>/', views.employeeDetails, name='employee_details'),

    # Route to add a new employee.
    # This will render the addEmployee view to display a form for creating a new employee.
    path('employee/add/', views.addEmployee, name='add_employee'),

    # Route to edit an existing employee's details.
    # The employee_id is passed in the URL to identify which employee to edit.
    path('employee/edit/<int:employee_id>/', views.editEmployee, name='edit_employee'),

    # Route to update the employment status of a specific employee.
    # The employee_id is passed in the URL to identify the employee whose status needs to be updated.
    path('employee/update_status/<int:employee_id>/', views.updateEmployeeStatus, name='update_employee_status'),

    # Route to generate a payroll for an employee.
    # This will render the generatePayroll view to generate and possibly display payroll information.
    path('employee/generate_payroll/', views.generatePayroll, name='generate_payroll'),
]
