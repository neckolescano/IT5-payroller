# ui/employee_form.py
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout
)

class EmployeeForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Employee")
        self.setModal(True)
        self.resize(300, 200)

        layout = QVBoxLayout()

        # Name
        self.name_input = QLineEdit()
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)

        # Position
        self.position_input = QLineEdit()
        layout.addWidget(QLabel("Position:"))
        layout.addWidget(self.position_input)

        # Rate per hour
        self.rate_input = QLineEdit()
        layout.addWidget(QLabel("Rate per hour:"))
        layout.addWidget(self.rate_input)

        # Hours worked
        self.hours_input = QLineEdit()
        layout.addWidget(QLabel("Hours Worked:"))
        layout.addWidget(self.hours_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.cancel_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self.accept)

    def get_data(self):
        return {
            "name": self.name_input.text(),
            "position": self.position_input.text(),
            "rate_per_hour": float(self.rate_input.text()),
            "hours_worked": float(self.hours_input.text())
        }
