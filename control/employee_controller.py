# control/employee_controller.py
import sqlite3
from datetime import datetime

from model.employee import Employee

class EmployeeController:
    def __init__(self, db_path="payroll.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

        self.employees = {}
        self.load_employees()

    def create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                position TEXT,
                rate_per_hour REAL,
                hours_worked REAL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS payroll_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                emp_id INTEGER,
                name TEXT,
                net_pay REAL,
                date TEXT
            );
        """)
        self.conn.commit()

    def load_employees(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, name, position, rate_per_hour, hours_worked FROM employees")
        rows = cur.fetchall()
        for r in rows:
            emp = Employee(r["id"], r["name"], r["position"], r["rate_per_hour"], r["hours_worked"])
            self.employees[emp.emp_id] = emp

    def add_employee(self, name, position, rate_per_hour, hours_worked):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO employees (name, position, rate_per_hour, hours_worked) VALUES (?, ?, ?, ?)",
            (name, position, rate_per_hour, hours_worked)
        )
        self.conn.commit()
        emp_id = cur.lastrowid
        emp = Employee(emp_id, name, position, rate_per_hour, hours_worked)
        self.employees[emp.emp_id] = emp
        return emp

    def get_employee(self, emp_id):
        return self.employees.get(emp_id)

    def get_all_employees(self):
        return list(self.employees.values())

    def update_employee(self, emp):
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE employees SET name=?, position=?, rate_per_hour=?, hours_worked=? WHERE id=?",
            (emp.name, emp.position, emp.rate_per_hour, emp.hours_worked, emp.emp_id)
        )
        self.conn.commit()
        self.employees[emp.emp_id] = emp

    def delete_employee(self, emp_id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM employees WHERE id=?", (emp_id,))
        self.conn.commit()
        if emp_id in self.employees:
            del self.employees[emp_id]

    def save_payroll_history(self, emp, net_pay):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO payroll_history (emp_id, name, net_pay, date) VALUES (?, ?, ?, ?)",
            (emp.emp_id, emp.name, net_pay, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        self.conn.commit()

    def get_payroll_history(self):
        cur = self.conn.cursor()
        cur.execute("SELECT emp_id, name,net_pay, date FROM payroll_history ORDER BY date DESC")
        return cur.fetchall()
