import datetime
from exceptions import DuplicatePatientError, BillingDataError

class Patient:
    def __init__(self, patient_id, name, age, department, doctor_id, admission_date, discharge_date, insurance_coverage, discount, consultation_fee, room_charge, diagnostic_fee, surgery_fee):
        self.patient_id = patient_id
        self.name = name
        self.age = int(age)
        self.department = department
        self.doctor_id = doctor_id
        self.admission_date = datetime.datetime.strptime(admission_date, '%Y-%m-%d') if admission_date else None
        self.discharge_date = datetime.datetime.strptime(discharge_date, '%Y-%m-%d') if discharge_date else None
        self.insurance_coverage = float(insurance_coverage)
        self.discount = float(discount)
        self.consultation_fee = float(consultation_fee)
        self.room_charge = float(room_charge)
        self.diagnostic_fee = float(diagnostic_fee)
        self.surgery_fee = float(surgery_fee)
        self.validate()

    def validate(self):
        if self.admission_date and self.admission_date > datetime.datetime.now():
            raise BillingDataError("Future admission date")
        if self.discharge_date and self.admission_date and self.discharge_date < self.admission_date:
            raise BillingDataError("Discharge before admission")
        # Add more validations as needed

    def calculate_total_bill(self):
        total = self.consultation_fee + self.room_charge + self.diagnostic_fee + self.surgery_fee - self.insurance_coverage - self.discount
        return total

class Doctor:
    def __init__(self, doctor_id, name, department, rating, punctuality, diagnosis_accuracy):
        self.doctor_id = doctor_id
        self.name = name
        self.department = department
        self.rating = float(rating)
        self.punctuality = float(punctuality)
        self.diagnosis_accuracy = float(diagnosis_accuracy)

    def get_score(self):
        # Simple score calculation
        return (self.rating + self.punctuality / 100 + self.diagnosis_accuracy / 100) / 3