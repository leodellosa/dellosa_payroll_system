from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('employees/', views.employeeList, name='employee_list'),
    # path('employee/<int:id>/', views.employeeDetails, name='employee_detail'),
    path('employee/add/', views.addEmployee, name='add_employee'),
    # path('employee/edit/<int:id>/', views.editEmployee, name='edit_employee'),
    # path('employee/delete/<int:id>/', views.deleteEmployee, name='delete_employee'),
]

