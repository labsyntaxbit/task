import argparse
from utils import read_csv, validate_data
from models import Patient, Doctor
from billing import BillingEngine
from reports import HospitalReportSystem

def main():
    parser = argparse.ArgumentParser(description='Hospital Management System')
    parser.add_argument('--month', type=str, help='Month for reports (e.g., march)')
    parser.add_argument('--department', type=str, help='Department for reports (e.g., cardiology)')
    args = parser.parse_args()

    # Load data
    patients = read_csv('data/patients.csv', Patient)
    doctors = read_csv('data/doctors.csv', Doctor)
    validate_data(patients, doctors)

    # Filter by month if provided
    if args.month:
        # Assuming admission_date month
        month_num = {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6, 'july':7, 'august':8, 'september':9, 'october':10, 'november':11, 'december':12}[args.month.lower()]
        patients = [p for p in patients if p.admission_date and p.admission_date.month == month_num]

    # Filter by department
    if args.department:
        patients = [p for p in patients if p.department == args.department]
        doctors = [d for d in doctors if d.department == args.department]

    billing_engine = BillingEngine(patients)
    report_system = HospitalReportSystem(doctors, billing_engine)

    # Generate reports
    print("Top 10 Rated Doctors:")
    for doc in report_system.top_rated_doctors(10):
        print(f"{doc.name}: {doc.get_score():.2f}")

    print("\nRevenue by Department:")
    revenue = report_system.revenue_by_department()
    for dept, rev in revenue.items():
        print(f"{dept}: {rev}")

    print("\nPatients Eligible for Discharge:")
    for p in report_system.patients_eligible_for_discharge():
        print(p.name)

    print("\nBilling Anomalies:")
    for anomaly in report_system.billing_anomalies_report():
        print(anomaly)

    print("\nCritical Patient Risk List:")
    for p in report_system.critical_patient_risk_list():
        print(p.name)

if __name__ == '__main__':
    main()