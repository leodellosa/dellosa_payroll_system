# Payroll System
### Description
This Payroll System is a web-based application designed to manage employee payrolls,generate payslips, and store employee information. It is built using Django for the backend and uses SQLite as the database for local development. The application is intended to run locally on your machine.

With this application, you can:
- Add, view, and manage employees.
- Generate payslips for employees.
- View employee details, payroll, and statuses.
- Export payslip as pdf or excel file
- Upload payroll details by batch using excel file with downloadable template

Features
### Done Development
- Employee Management: Add, view, and manage employee details.
- Build the generate payroll feature and viewing of payroll summary
- Payslip export to pdf or excel
- Batch upload of payroll via excel file

#### Done Task
- Separate payroll from employee and enhance app design
- Build export payroll records to excel or pdf feature
- Add date filter in payroll summary view
- Add download template button for batch upload
- Add Batch upload of payrolls via excel

#### Nice to have feature
- Settings
- Log in Log out

#### Note:
Currently, the app supports only admin users. Future updates may include role-based access control.


Prerequisites
- Python: Make sure Python 3.8+ is installed. You can download it from python.org.
- Pip: Ensure that pip is installed to manage Python packages. You can install pip by following this guide.

Installation
1. Clone this repository to your local machine:
- git clone https://github.com/leodellosa/dellosa_payroll_system.git
- cd payroll-system

2. Create a virtual environment to isolate project dependencies:
- python -m venv venv

3. Activate the virtual environment:
- venv\Scripts\activate

4. Install the required Python packages:
- pip install -r requirements.txt

5. Apply migrations to set up the SQLite database:
- python manage.py migrate

6. Create a superuser account to access the Django admin:
- python manage.py createsuperuser
- Follow the prompts to set up the superuser credentials.

7. Run the Django development server:
- python manage.py runserver
- The application will now be available at http://localhost:8000.

8. Accessing Django Admin
Once the server is running, you can access the Django Admin by visiting http://localhost:8000/admin/ and logging in with the superuser credentials you just created. From there, you can manage employees and payroll data.

9. Stopping the Application
To stop the development server, simply press Ctrl+C in your terminal.


