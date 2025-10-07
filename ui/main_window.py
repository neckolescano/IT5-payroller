# ui/main_window.py
from datetime import datetime

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QStackedWidget,
)
from PyQt6.QtGui import QFont, QPixmap, QMovie
from PyQt6.QtCore import Qt, QSize

from ui.employee_form import EmployeeForm
from ui.generate_payroll import GeneratePayrollWidget


class MainWindow(QMainWindow):
    def __init__(self, employee_controller):
        super().__init__()

        # --- Stylesheet ---
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: 'Courier New';  
                font-size: 12pt;             
            }
            QLabel {
                color: #ffffff;
                font-weight: bold;
                font-family: 'Courier New';
            }
            QPushButton {
                background-color: #555555;
                color: #ffffff;
                border-radius: 6px;
                padding: 6px 12px;
                font-family: 'Courier New';
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #777777;
            }
            QTableWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                gridline-color: #555555;
                border: 1px solid #555555;
                alternate-background-color: #3a3a3a;
                font-family: 'Courier New';
                font-size: 12pt;
            }
            QHeaderView::section {
                background-color: #555555;
                color: #ffffff;
                padding: 6px;
                border: none;
                font-family: 'Courier New';
                font-weight: bold;
            }
            QComboBox, QLineEdit {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 4px;
                border-radius: 4px;
                font-family: 'Courier New';
            }
        """)

        self.employee_controller = employee_controller
        self.setWindowTitle("Payroll System")
        self.setGeometry(100, 100, 1100, 700)

        font = QFont("Courier New", 12)
        self.setFont(font)

        # --- Central widget ---
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # --- Banner (Top Image) ---
        self.banner = QLabel()
        self.banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.banner.setPixmap(QPixmap("assets/ayRoller.png").scaledToHeight(120, Qt.TransformationMode.SmoothTransformation))
        self.main_layout.addWidget(self.banner)

        # --- Navigation buttons ---
        nav_layout = QHBoxLayout()
        self.btn_home = QPushButton("Home")
        self.btn_employees = QPushButton("Employees")
        self.btn_history = QPushButton("Payroll History")
        self.btn_summary = QPushButton("Summary")

        for btn in [self.btn_home, self.btn_employees, self.btn_history, self.btn_summary]:
            btn.setStyleSheet("padding: 8px 16px; font-weight: bold;")
            nav_layout.addWidget(btn)

        self.main_layout.addLayout(nav_layout)

        # --- Stacked pages ---
        self.stacked = QStackedWidget()
        self.main_layout.addWidget(self.stacked)

        # --- Page 1: Home ---
        self.page_home = QWidget()
        home_layout = QVBoxLayout(self.page_home)
        home_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a container widget to center content
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Add GIF animation ---
        self.logo_gif = QLabel()
        self.logo_gif.setAlignment(Qt.AlignmentFlag.AlignCenter)

        movie = QMovie("assets/ayRoller (3).gif")
        movie.setCacheMode(QMovie.CacheMode.CacheAll)

        # Directly set scaled size (width x height)
        target_width = 250
        target_height = 120
        movie.setScaledSize(QSize(target_width, target_height))

        self.logo_gif.setMovie(movie)
        movie.start()

        # --- Welcome text ---
        home_label = QLabel("Welcome to the PayRoller System")
        home_label.setFont(QFont("Courier New", 25, QFont.Weight.Bold))
        home_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        details_label = QLabel("Manage employees, track payroll history, and view salary summaries.")
        details_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Add widgets to center layout ---
        center_layout.addWidget(self.logo_gif)
        center_layout.addSpacing(20)
        center_layout.addWidget(home_label)
        center_layout.addWidget(details_label)

        # Add stretch above and below to center vertically
        home_layout.addStretch()
        home_layout.addWidget(center_widget)
        home_layout.addStretch()

        self.stacked.addWidget(self.page_home)

        # --- Page 2: Employees ---
        self.page_employees = QWidget()
        emp_outer_layout = QHBoxLayout(self.page_employees)

        # Left side: Table
        self.left_layout = QVBoxLayout()
        self.label = QLabel("Employees")
        self.label.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        self.left_layout.addWidget(self.label)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Name", "Position", "Rate per Hour", "Net Pay"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.left_layout.addWidget(self.table)

        self.add_button = QPushButton("Add Employee")
        self.add_button.clicked.connect(self.add_employee_ui)
        self.left_layout.addWidget(self.add_button)

        emp_outer_layout.addLayout(self.left_layout)

        # Right side: Payroll generator
        self.generate_widget = GeneratePayrollWidget(self.employee_controller)
        self.generate_widget.setMaximumWidth(340)
        emp_outer_layout.addWidget(self.generate_widget)

        self.stacked.addWidget(self.page_employees)

        # --- Page 3: Payroll History ---
        self.page_history = QWidget()
        hist_layout = QVBoxLayout(self.page_history)

        self.history_label = QLabel("Payroll History")
        self.history_label.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        hist_layout.addWidget(self.history_label)

        self.history_table = QTableWidget(0, 5)
        self.history_table.setHorizontalHeaderLabels(["Name", "Position", "Hours Worked", "Net Pay", "Date"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        hist_layout.addWidget(self.history_table)

        self.stacked.addWidget(self.page_history)

        # --- Page 4: Summary ---
        self.page_summary = QWidget()
        sum_layout = QVBoxLayout(self.page_summary)
        sum_layout.addStretch()

        sum_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center content vertically

        # Create a receipt-style container
        receipt_widget = QWidget()
        receipt_widget.setFixedWidth(600)
        receipt_layout = QVBoxLayout(receipt_widget)
        receipt_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        receipt_widget.setStyleSheet("""
            background-color: #2b2b2b;  /* Dark gray background */
            border: 2px solid #555555;  /* Receipt border */
            border-radius: 8px;
            padding: 20px;
        """)

        # Receipt Title
        self.summary_label = QLabel("Payroll Summary")
        self.summary_label.setFont(QFont("Courier New", 16, QFont.Weight.Bold))  # Monospace like receipt
        self.summary_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        receipt_layout.addWidget(self.summary_label)
        receipt_layout.addSpacing(10)

        # Receipt items
        self.total_employees = QLabel("Total Employees: 0")
        self.total_payroll = QLabel("Total Payroll: 0.00")
        self.average_pay = QLabel("Average Pay: 0.00")
        self.highest_salary = QLabel("Highest Salary: 0.00")

        for lbl in [self.total_employees, self.total_payroll, self.average_pay, self.highest_salary]:
            lbl.setFont(QFont("Courier New", 12))  # Monospace
            lbl.setAlignment(Qt.AlignmentFlag.AlignLeft)
            receipt_layout.addWidget(lbl)
            receipt_layout.addSpacing(5)

        # Optional: add a footer line like a receipt
        footer = QLabel("Thank you for using PayRoller!")
        footer.setFont(QFont("Courier New", 10, QFont.Weight.Bold))
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        receipt_layout.addSpacing(15)
        receipt_layout.addWidget(footer)

        # Center receipt widget in the page
        sum_layout.addStretch()
        sum_layout.addWidget(receipt_widget)
        sum_layout.addStretch()


        self.stacked.addWidget(self.page_summary)

        # --- Connect nav buttons ---
        self.btn_home.clicked.connect(lambda: self.show_page(self.page_home))
        self.btn_employees.clicked.connect(lambda: self.show_page(self.page_employees))
        self.btn_history.clicked.connect(lambda: self.show_page(self.page_history))
        self.btn_summary.clicked.connect(lambda: self.show_page(self.page_summary))

        # Start on Home
        self.show_page(self.page_home)

    # --- Functions ---
    def show_page(self, page):
        self.stacked.setCurrentWidget(page)
        if page == self.page_employees:
            self.refresh_table()
        elif page == self.page_history:
            self.refresh_history()
        elif page == self.page_summary:
            self.refresh_summary()

    def refresh_table(self):
        employees = self.employee_controller.get_all_employees()
        self.table.setRowCount(len(employees))
        for row, emp in enumerate(employees):
            self.table.setItem(row, 0, QTableWidgetItem(emp.name))
            self.table.setItem(row, 1, QTableWidgetItem(emp.position))
            self.table.setItem(row, 2, QTableWidgetItem(str(emp.rate_per_hour)))
            self.table.setItem(row, 3, QTableWidgetItem(f"{emp.compute_salary():.2f}"))

        try:
            self.generate_widget.refresh_employee_list()
        except Exception:
            pass

    def refresh_history(self):
        history = self.employee_controller.get_payroll_history()
        self.history_table.setRowCount(len(history))

        for row, record in enumerate(history):
            emp_id, name, net_pay, date_text = record

            emp = self.employee_controller.get_employee(emp_id)

            if emp:
                self.history_table.setItem(row, 0, QTableWidgetItem(emp.name))
                self.history_table.setItem(row, 1, QTableWidgetItem(emp.position))
                self.history_table.setItem(row, 2, QTableWidgetItem(str(emp.hours_worked)))
                self.history_table.setItem(row, 3, QTableWidgetItem(f"{emp.compute_salary():.2f}"))
            else:
                # fallback if employee was deleted
                self.history_table.setItem(row, 0, QTableWidgetItem(name))
                self.history_table.setItem(row, 1, QTableWidgetItem(""))
                self.history_table.setItem(row, 2, QTableWidgetItem("0"))
                self.history_table.setItem(row, 3, QTableWidgetItem(f"{float(net_pay):.2f}"))


            self.history_table.setItem(row, 4, QTableWidgetItem(date_text))

    def refresh_summary(self):
        employees = self.employee_controller.get_all_employees()
        if not employees:
            self.total_employees.setText("Total Employees: 0")
            self.total_payroll.setText("Total Payroll: 0.00")
            self.average_pay.setText("Average Pay: 0.00")
            self.highest_salary.setText("Highest Salary: 0.00")
            return

        total_emp = len(employees)
        total_pay = sum(emp.compute_salary() for emp in employees)
        avg_pay = total_pay / total_emp
        high_salary = max(emp.compute_salary() for emp in employees)

        self.total_employees.setText(f"Total Employees: {total_emp}")
        self.total_payroll.setText(f"Total Payroll: {total_pay:.2f}")
        self.average_pay.setText(f"Average Pay: {avg_pay:.2f}")
        self.highest_salary.setText(f"Highest Salary: {high_salary:.2f}")

    def add_employee_ui(self):
        dialog = EmployeeForm(self)
        if dialog.exec():
            data = dialog.get_data()
            self.employee_controller.add_employee(
                name=data["name"],
                position=data["position"],
                rate_per_hour=data["rate_per_hour"],
                hours_worked=data["hours_worked"]
            )
            self.refresh_table()
