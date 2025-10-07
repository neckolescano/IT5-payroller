# ui/generate_payroll.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox,
    QFormLayout, QLineEdit, QPushButton, QMessageBox
)

class GeneratePayrollWidget(QWidget):
    def __init__(self, employee_controller, parent=None):
        super().__init__(parent)
        self.employee_controller = employee_controller

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Select Employee:"))

        self.employee_combo = QComboBox()
        layout.addWidget(self.employee_combo)

        form = QFormLayout()
        self.rate_input = QLineEdit()
        self.hours_input = QLineEdit()
        form.addRow("Rate per Hour:", self.rate_input)
        form.addRow("Hours Worked:", self.hours_input)
        layout.addLayout(form)

        self.btn_generate = QPushButton("Generate Payroll")
        self.btn_generate.clicked.connect(self.generate_payroll)
        layout.addWidget(self.btn_generate)

        self.btn_clear = QPushButton("Clear Inputs")
        self.btn_clear.clicked.connect(self.clear_inputs)
        layout.addWidget(self.btn_clear)

        self.btn_delete = QPushButton("Delete Employee")
        self.btn_delete.clicked.connect(self.delete_employee)
        layout.addWidget(self.btn_delete)

        self.refresh_employee_list()
        self.employee_combo.currentIndexChanged.connect(self.prefill_fields)

    def refresh_employee_list(self):
        self.employee_combo.clear()
        for emp in self.employee_controller.get_all_employees():
            self.employee_combo.addItem(emp.name, emp.emp_id)
        self.prefill_fields()

    def prefill_fields(self):
        emp = self.employee_controller.get_employee(self.employee_combo.currentData())
        if emp:
            self.rate_input.setText(str(emp.rate_per_hour))
            self.hours_input.setText(str(emp.hours_worked))

    def generate_payroll(self):
        emp = self.employee_controller.get_employee(self.employee_combo.currentData())
        if not emp:
            return
        try:
            emp.rate_per_hour = float(self.rate_input.text())
            emp.hours_worked = float(self.hours_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Enter valid numbers")
            return

        self.employee_controller.update_employee(emp)
        total = emp.compute_salary()

        # Save payroll history
        self.employee_controller.save_payroll_history(emp, total)

        QMessageBox.information(
            self,
            "Payroll",
            f"{emp.name}\nRate: {emp.rate_per_hour}\nHours: {emp.hours_worked}\nNet Pay: {total:.2f}"
        )

        mainwin = self.window()
        if hasattr(mainwin, "refresh_table"):
            mainwin.refresh_table()
        if hasattr(mainwin, "refresh_history"):
            mainwin.refresh_history()
        if hasattr(mainwin, "refresh_summary"):
            mainwin.refresh_summary()

        self.refresh_employee_list()

    def clear_inputs(self):
        self.rate_input.clear()
        self.hours_input.clear()
        self.employee_combo.setCurrentIndex(-1)

    def delete_employee(self):
        emp = self.employee_controller.get_employee(self.employee_combo.currentData())
        if not emp:
            QMessageBox.warning(self, "Error", "No employee selected")
            return

        self.employee_controller.delete_employee(emp.emp_id)
        QMessageBox.information(self, "Deleted", f"{emp.name} was removed.")

        mainwin = self.window()
        if hasattr(mainwin, "refresh_table"):
            mainwin.refresh_table()
        self.refresh_employee_list()
