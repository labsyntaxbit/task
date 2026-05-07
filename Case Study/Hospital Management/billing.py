from models import Patient
from exceptions import BillingDataError

class BillingEngine:
    def __init__(self, patients):
        self.patients = patients

    def calculate_bills(self):
        bills = {}
        for patient in self.patients:
            bills[patient.patient_id] = patient.calculate_total_bill()
        return bills

    def detect_anomalies(self):
        anomalies = []
        for patient in self.patients:
            bill = patient.calculate_total_bill()
            if bill < 0:
                anomalies.append(f"Negative bill amount for patient {patient.patient_id}")
            if patient.diagnostic_fee > 1000:  # Example threshold
                anomalies.append(f"High diagnostic fee for patient {patient.patient_id}")
            if patient.discharge_date and patient.room_charge > 0 and (patient.discharge_date - patient.admission_date).days < 1:
                anomalies.append(f"Full room charge for short stay patient {patient.patient_id}")
            # Check for duplicate insurance claims, etc.
        return anomalies