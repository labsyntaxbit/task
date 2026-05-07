import csv
import json
from models import Patient, Doctor
from exceptions import DuplicatePatientError

def read_csv(file_path, model_class):
    items = []
    ids = set()
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if model_class == Patient:
                item = Patient(**row)
                id_field = item.patient_id
            elif model_class == Doctor:
                item = Doctor(**row)
                id_field = item.doctor_id
            if id_field in ids:
                raise DuplicatePatientError(f"Duplicate ID: {id_field}")
            ids.add(id_field)
            items.append(item)
    return items

def validate_data(patients, doctors):
    # Check missing doctor assignment
    doctor_ids = {d.doctor_id for d in doctors}
    for p in patients:
        if p.doctor_id not in doctor_ids:
            raise ValueError(f"Missing doctor assignment for patient {p.patient_id}")

def department_hierarchy():
    # Simple hierarchy: cardiology under medicine, etc.
    hierarchy = {
        'cardiology': 'medicine',
        'orthopedics': 'surgery',
        'neurology': 'medicine'
    }
    return hierarchy

def traverse_department(dept, hierarchy, result=None):
    if result is None:
        result = []
    result.append(dept)
    if dept in hierarchy:
        traverse_department(hierarchy[dept], hierarchy, result)
    return result