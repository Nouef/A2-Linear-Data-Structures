import tkinter as tk
from tkinter import messagebox, simpledialog

class Patient:
    def __init__(self, patient_id, name, medical_condition, admission_date):
        self.patient_id = patient_id
        self.name = name
        self.medical_condition = medical_condition
        self.admission_date = admission_date

class Doctor:
    def __init__(self, doctor_id, name):
        self.doctor_id = doctor_id
        self.name = name

class Appointment:
    def __init__(self, patient_id, doctor_id, details):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.details = details
        self.prescription = None

class HospitalSystem:
    def __init__(self):
        self.patients = []
        self.waiting_queue = []
        self.prescriptions_stack = []
        self.appointments = []
        self.doctors = [
            Doctor(1, "Dr. Smith"),
            Doctor(2, "Dr. Johnson"),
            Doctor(3, "Dr. Wilson")
        ]

    def add_patient(self, patient):
        # Check if a patient with the given ID already exists
        for existing_patient in self.patients:
            if existing_patient.patient_id == patient.patient_id:
                return False
        self.patients.append(patient)
        self.waiting_queue.append(patient)
        return True

    def remove_patient(self, patient_id):
        patient_to_remove = None
        for patient in self.patients:
            if patient.patient_id == patient_id:
                patient_to_remove = patient
                break
        if patient_to_remove:
            self.patients.remove(patient_to_remove)
            try:
                self.waiting_queue.remove(patient_to_remove)
            except ValueError:
                pass
            return True
        return False

    def schedule_appointment(self, patient_id, doctor_id):
        for patient in self.patients:
            if patient.patient_id == patient_id:
                doctor = next((doc for doc in self.doctors if doc.doctor_id == doctor_id), None)
                if doctor:
                    appointment = Appointment(patient_id, doctor_id, f"Patient: {patient.name}, Doctor: {doctor.name}")
                    self.appointments.append(appointment)
                    return f"Appointment Scheduled: {appointment.details}"
        return "Patient or doctor not found"

    def issue_prescription(self, patient_id, medication):
        for appointment in self.appointments:
            if appointment.patient_id == patient_id and not appointment.prescription:
                appointment.prescription = medication
                self.prescriptions_stack.append(appointment)
                return True
        return False
        def get_waiting_queue(self):
        return [patient.name for patient in self.waiting_queue]

    def process_next_patient(self):
        if self.waiting_queue:
            patient = self.waiting_queue.pop(0)
            return patient
        return None

    def get_appointments_with_prescriptions(self):
        results = []
        for appointment in self.prescriptions_stack:
            patient_name = next((patient.name for patient in self.patients if patient.patient_id == appointment.patient_id), "Unknown")
            doctor_name = next((doctor.name for doctor in self.doctors if doctor.doctor_id == appointment.doctor_id), "Unknown")
            prescription = "Pending" if not appointment.prescription else appointment.prescription
            results.append(f"Patient: {patient_name}, Doctor: {doctor_name}, Prescription: {prescription}")
        return results

initial_patients_data = [
    (101, "John Doe", "Fever", "2024-03-15"),
    (102, "Alice Smith", "Broken Arm", "2024-03-17"),
    (103, "Bob Johnson", "Flu", "2024-03-20"),
    (104, "Emily Brown", "Migraine", "2024-03-22"),
    (105, "David Wilson", "Diabetes", "2024-03-25")
]

class HospitalSystemGUI:
    def __init__(self, root):
        self.root = root
        self.hospital_system = HospitalSystem()
        for data in initial_patients_data:
            patient = Patient(*data)
            self.hospital_system.add_patient(patient)
        self.root.title("Hospital Management System")
        self.root.geometry("500x500")

        tk.Button(self.root, text="Process Next Patient", command=self.process_next_patient).pack(fill=tk.X)

        self.queue_frame = tk.LabelFrame(self.root, text="Waiting Queue")
        self.queue_frame.pack(pady=10)
        self.queue_listbox = tk.Listbox(self.queue_frame, width=50)
        self.queue_listbox.pack()
        self.update_queue_listbox()

        tk.Button(self.root, text="Add New Patient", command=self.add_patient_window).pack(fill=tk.X)
        tk.Button(self.root, text="Remove Patient", command=self.remove_patient).pack(fill=tk.X)
        tk.Button(self.root, text="Schedule Appointment", command=self.schedule_appointment_window).pack(fill=tk.X)
        tk.Button(self.root, text="Issue Prescription", command=self.issue_prescription_window).pack(fill=tk.X)
        tk.Button(self.root, text="View Appointments", command=self.view_appointments_window).pack(fill=tk.X)
