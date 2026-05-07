class DiagnosticLab:
    def __init__(self):
        self.reports = {}

    def generate_report(self, patient_id, results):
        self.reports[patient_id] = results

    def get_report(self, patient_id):
        return self.reports.get(patient_id, "No report available")