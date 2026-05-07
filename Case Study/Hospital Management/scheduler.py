import datetime

class AppointmentScheduler:
    def __init__(self):
        self.appointments = []

    def schedule_appointment(self, patient_id, doctor_id, date):
        self.appointments.append({
            'patient_id': patient_id,
            'doctor_id': doctor_id,
            'date': datetime.datetime.strptime(date, '%Y-%m-%d')
        })

    def get_appointments(self, doctor_id=None, date=None):
        filtered = self.appointments
        if doctor_id:
            filtered = [a for a in filtered if a['doctor_id'] == doctor_id]
        if date:
            filter_date = datetime.datetime.strptime(date, '%Y-%m-%d')
            filtered = [a for a in filtered if a['date'].date() == filter_date.date()]
        return filtered