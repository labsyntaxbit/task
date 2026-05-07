from models import Doctor
from billing import BillingEngine

class HospitalReportSystem:
    def __init__(self, doctors, billing_engine):
        self.doctors = doctors
        self.billing_engine = billing_engine

    def top_rated_doctors(self, n=10):
        sorted_doctors = sorted(self.doctors, key=lambda d: d.get_score(), reverse=True)
        return sorted_doctors[:n]

    def revenue_by_department(self):
        revenue = {}
        bills = self.billing_engine.calculate_bills()
        for patient in self.billing_engine.patients:
            dept = patient.department
            revenue[dept] = revenue.get(dept, 0) + bills.get(patient.patient_id, 0)
        return revenue

    def patients_eligible_for_discharge(self):
        # Simple logic: patients with discharge_date set
        return [p for p in self.billing_engine.patients if p.discharge_date]

    def billing_anomalies_report(self):
        return self.billing_engine.detect_anomalies()

    def critical_patient_risk_list(self):
        # Example: patients 60 and over
        return [p for p in self.billing_engine.patients if p.age >= 60]