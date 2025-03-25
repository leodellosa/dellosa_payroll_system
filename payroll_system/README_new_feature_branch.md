# New Features for Payroll System

## Project Overview

This README is specific to the **feature branch** where new features have been implemented for the **Payroll System**. The primary focus of this feature branch is to enhance the employee list functionality by adding **search** and **filter** features.

### Features Implemented

- **Employee Search**: Allows searching for employees by their **first name** and **last name**.
- **Hire Date Filter**: Filters employees based on their hire date range.
- **Status Filter**: Filters employees by their status (e.g., Active or Inactive).
- **Apply Filters**: Users can apply all the filters (search, hire date, and status) using a single button.
- **Clear Filters**: A button to clear all applied filters and reset the employee list.

---

## Current Build (Filters)

In the current build of the project, we have added the following features:

1. **Employee Search**:
    - A text input field that allows users to search for employees by their **first name** and **last name**.
    
2. **Hire Date Filter**:
    - Two date input fields allow users to filter employees based on their **hire date**. Users can set a date range with a start date and end date.
    
3. **Status Filter**:
    - A dropdown menu to filter employees based on their **status** (Active or Inactive).
    
4. **Apply Button**:
    - Once the user has entered a search term, selected a date range, and/or chosen a status, they can click the "Apply Filter" button to filter the employee list based on those criteria.
    - The **Apply Filter** button is only enabled when at least one filter has a value (search, hire date, or status).
    
5. **Clear Filters Button**:
    - A "Clear" button to reset all filters and display the full employee list again.

---

## How to Use the Features

1. **Search Employees**:
   - Enter a **first name** or **last name** in the search bar to filter employees by name.
   
2. **Filter by Hire Date**:
   - Select a **start date** and an **end date** in the date filters to filter employees by their hire date range.
   
3. **Filter by Status**:
   - Choose **Active** or **Inactive** from the status dropdown to filter employees by their employment status.
   
4. **Apply Filters**:
   - After entering the required values in any of the fields, click the **Apply Filter** button to apply the selected filters.
   
5. **Clear Filters**:
   - Click the **Clear** button to reset all the filters and display the full list of employees.

---

## How to Test the Features

1. **Run the Application**:
   - Ensure your Django application is set up and running.
   - Navigate to the **Employee List** page.

2. **Testing the Filters**:
   - Test the **search functionality** by typing different names in the search bar.
   - Test the **hire date filter** by selecting various date ranges and verifying that the list updates accordingly.
   - Test the **status filter** by choosing **Active** or **Inactive** and verifying that the list updates accordingly.
   - Ensure that the **Apply Filter** button works only when there is at least one filter selected and resets when all fields are cleared.

---

## Future Improvements

- Add the ability to **export filtered employee data** to CSV, Excel, or PDF format.
- Improve **UI/UX** for better user experience with filters.
- Optimize the filter query for larger datasets to enhance performance.
  
---

## Installation and Setup

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

