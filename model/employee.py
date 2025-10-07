class Employee:
    def __init__(self, emp_id, name, position, rate_per_hour, hours_worked=0):
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.rate_per_hour = rate_per_hour
        self.hours_worked = hours_worked

    def add_hours(self, hours):
        self.hours_worked += hours

    def reset_hours(self):
        self.hours_worked = 0

    def compute_salary(self):
        gross = self.rate_per_hour * self.hours_worked
        deductions = gross * 0.10
        return gross - deductions



