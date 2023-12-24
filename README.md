# Vanvas Attendance Management System Documentation
## Introduction
Vanvas is an Attendance Management System implemented in Python using the Tkinter library for the graphical user interface and MySQL for database management. It provides functionalities such as adding students, deleting students, marking attendance, and viewing attendance reports.

### Prerequisites
 - Python
 - Tkinter
 - MySQL
 - Tkcalendar
 - mysql-connector

### Files
 - vanvas.py: The main Python script containing the implementation of the Vanvas Attendance Management System.
 - vanvasMySQLdumps.sql: A MySQL dump file containing the database schema and sample data.
  
## Installation
- Install Python: Python Downloads
- Install Tkinter: Tkinter is included with most Python installations.
- Install Tkcalendar: pip install tkcalendar
- Install mysql-connector: pip install mysql-connector-python
- Import the MySQL dump file into your MySQL database.
### Database Setup
- Create a MySQL database named 'vanvas'.
- Execute the following command in your MySQL console to import the database schema and sample data:
sql
```source path/to/vanvasMySQLdumps.sql;```

### Running the Application
Open a terminal and navigate to the directory containing the 'vanvas.py' script.
Run the command: ```python vanvas.py```

## Features
### Add Student:
- Clicking the "Add Student" button opens a new window where you can enter the student's name, admission number, class, and section.
- Clicking the "SAVE" button adds the student to the database.

### Delete Student:
- Clicking the "Delete Student" button opens a new window where you can enter the admission number of the student to be deleted.
- Clicking the "Check Student" button verifies the existence of the student.
- Confirming the deletion removes the student from the database.

### Mark Attendance:
- Clicking the "Mark Attendance" button opens a new window with options to select the class, section, and date.
- Clicking the "Select" button displays a list of students in the selected class and section.
- After selecting attendance (Present or Absent) for each student, clicking the "Save Attendance" button saves the data to the database.

### View Report:
- Clicking the "View Report" button opens a new window where you can select the class, section, month, and year.
- Clicking the "Select" button displays a report showing the total number of days each student was present and absent for the selected month and year.

## Note
- The Tkcalendar library is used for date selection in the "Mark Attendance" section.
- The MySQL database is used to store student information and attendance records.
- This documentation assumes a basic understanding of Python, Tkinter, MySQL, and the command line interface. Make sure to replace "path/to/vanvasMySQLdumps.sql" with the actual path to the MySQL dump file.

## Conclusion
Vanvas is a simple attendance management system that provides essential features for tracking student attendance. It offers a user-friendly interface for adding, deleting students, marking attendance, and generating reports. The MySQL database ensures data persistence and reliability.
