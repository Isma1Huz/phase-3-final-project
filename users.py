import datetime
import sqlite3
import shutil
import time

def center_text(text):
    terminal_width, _ = shutil.get_terminal_size()
    padding = max(0, (terminal_width - len(text)) // 2)
    centered_text = " " * padding + text
    print(centered_text)

# Function to display the clock and text
def display_clock_and_text():
        # Get the current time
        current_time = time.strftime("%H:%M:%S")

        # Clear the screen
        print("\033c", end="")

        clock = f"""
                                                            .---.
                                                           /     \\
                                                           |  {current_time}  
                                                           \\     /
                                                            '---'
"""
        
        print(("  " * 120  +  clock))

# Call the function to display the clock and text
display_clock_and_text()


def center_text(text):
    terminal_width, _ = shutil.get_terminal_size()
    padding = max(0, (terminal_width - len(text)) // 2)
    centered_text = " " * padding + text
    print(centered_text)

# Create a SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create tables for employees and admins if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT,
        employee_name TEXT,
        employee_email TEXT,
        department TEXT,
        password TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_id TEXT,
        admin_name TEXT,
        password TEXT
    )
''')
conn.commit()


def EmployeeLogin(employee_id, employee_password):
    # Check employee credentials in the database
    cursor.execute('SELECT * FROM employees WHERE employee_id=? AND password=?', (employee_id, employee_password))
    employee = cursor.fetchone()

    if employee:
        return employee
    else:
        return None

def AdminLogin(admin_id, admin_password):
    # Check admin credentials in the database
    cursor.execute('SELECT * FROM admins WHERE admin_id=? AND password=?', (admin_id, admin_password))
    admin = cursor.fetchone()

    if admin:
        return admin
    else:
        return None

def CreateEmployee():
    employee_id = input("Enter new employee ID: ")
    employee_name = input("Enter employee name: ")
    employee_email = input("Enter employee email: ")
    department = input("Enter department: ")
    employee_password = input("Enter employee password: ")

    # Insert the new employee record into the database
    cursor.execute('''
        INSERT INTO employees (employee_id, employee_name, employee_email, department, password)
        VALUES (?, ?, ?, ?, ?)
    ''', (employee_id, employee_name, employee_email, department, employee_password))
    conn.commit()

    print("Employee created successfully.")

# Header
def center(text):
    print(text.center(127))

def header(center_func):
    line = '=' * 127  # Full-width line for separation
    center_func(line)
    center_func("Welcome to the Time Tracking and Attendance System")
    center_func("Please follow the instructions below")
    center_func("Please login below with your employee id and password")
    center_func("NOTE: You cannot login if you are NOT an employee of this company.")
    center_func("If you are the administrator, you can log in and generate the attendance report.")
    center_func("Please select if you are an employee or an administrator to continue:")
    center_func(line)


# Function to generate an attendance report
def generate_attendance_report():
    cursor.execute('''
        SELECT attendance.employee_id, attendance.time_in, employees.employee_name
        FROM attendance
        INNER JOIN employees ON attendance.employee_id = employees.employee_id
    ''')
    records = cursor.fetchall()

    if not records:
        print("No attendance records found.")
        return

    center("Attendance Report:")
    print("{:<15} {:<30} {:<20} {:<25}".format("Employee ID", "Employee Name", "Department", "Email address",  "Date", "Time In"))
    print("=" * 90)

    for record in records:
        employee_id, time_in, employee_name = record[0], record[1], record[2]
        date, time = time_in.split(" ")
        print("{:<15} {:<30} {:<20} {:<25}".format(employee_id, employee_name, date, time))

    conn.close()

header(center)
center("1 - Employee")
center("2 - Administrator")
selection = input("Enter your selection number: ")
# Function to log attendance
def log_attendance(employee_id, time_in):
    conn = sqlite3.connect('database.db') 
    cursor = conn.cursor()

    # Create the 'attendance' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT,
            time_in TIMESTAMP
        )
    ''')

    # Insert a new record into the 'attendance' table
    cursor.execute('INSERT INTO attendance (employee_id, time_in) VALUES (?, ?)', (employee_id, time_in))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

if selection == "1":
    employee_id = input("Enter employee ID: ")
    employee_password = input("Enter employee password: ")

    employee = EmployeeLogin(employee_id, employee_password)

    if employee:
        center(f"Welcome {employee[2]}")
        center("You have logged in as an employee.")
         # Get the current timestamp
        sign_in_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Print the sign-in time
        center(f"Your sign-in time: {sign_in_time}")

        # Log the attendance in the database
        log_attendance(employee_id=employee_id, time_in=sign_in_time)
    else:
        center("Invalid employee credentials")

elif selection == "2":
    admin_id = input("Enter admin ID: ")
    admin_password = input("Enter admin password: ")

    admin = AdminLogin(admin_id, admin_password)

    if admin:
        center(f"Welcome {admin[2]}")
        center("You have logged in as an administrator.")
        line = '=' * 127  # Full-width line for separation
        center("Please select your options")
        center("1 - Add a new employee")
        center("2 - Generate attendance report")
        select = input("Enter the selection: ")
        if select == "1":
            CreateEmployee()  # Allow admin to create new employee
        elif select == "2":
            generate_attendance_report()
        else:
            center("Invalid selection")


    else:
        center("Invalid admin credentials")

else:
    center("Invalid selection")

# Close the database connection when done
conn.close()












