from django.contrib import admin
from .models import Employee, Payroll

# Register the models so that they appear in the admin interface

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'hire_date')  # Columns to show in the list view
    search_fields = ('first_name', 'last_name', 'email')  # Fields you can search by
    list_filter = ('hire_date',)  # Filter by hire date

# Register the custom admin class with the model
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Payroll)

