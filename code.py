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
        self.patients = {}
        self.doctors = {1: Doctor(1, "Dr. Smith", "Cardiology"), 2: Doctor(2, "Dr. Johnson", "Neurology"), 3: Doctor(3, "Dr. Wilson", "General Medicine")}
        self.appointments = deque()  # Using a deque as a queue for appointments
        self.prescriptions_stack = []  # Using a list as a stack for prescriptions
        self.add_initial_data()
    def add_initial_data(self):
        initial_patients = [
            ("Alice", "Flu", "2023-04-01", 1, "2023-04-02"),
            ("Bob", "Cold", "2023-04-01", 2, "2023-04-03"),
            ("Charlie", "Fever", "2023-04-02", 3, "2023-04-03"),
            ("Diana", "Injury", "2023-04-02", 1, "2023-04-04"),
            ("Ethan", "Checkup", "2023-04-03", 2, "2023-04-05"),
        ]
        for patient_id, (name, condition, admission_date, doctor_id, appointment_date) in enumerate(initial_patients, start=1):
            self.add_patient(name, condition, admission_date, doctor_id, appointment_date, patient_id)
            self.schedule_appointment(patient_id, doctor_id, appointment_date)  # Schedules their appointment

    def add_initial_data(self):
        initial_data = [("Alice", "Flu", "2023-04-01"), ("Bob", "Cold", "2023-04-02"), ("Charlie", "Fever", "2023-04-03"), ("Diana", "Injury", "2023-04-04"), ("Ethan", "Checkup", "2023-04-05")]
        for patient_id, (name, condition, admission_date) in enumerate(initial_data, start=1):
            self.patients[patient_id] = Patient(patient_id, name, condition, admission_date)

    def consult_next_patient(self, doctor_id):
        for i, appt in enumerate(self.appointments):
            if appt.doctor_id == doctor_id and appt.prescription is None:
                return self.appointments.pop(i)
        return None

    def add_patient(self, name, condition, admission_date):
        patient_id = max(self.patients.keys(), default=0) + 1
        self.patients[patient_id] = Patient(patient_id, name, condition, admission_date)
        messagebox.showinfo("Success", f"Patient {name} added successfully.")

    def schedule_appointment(self, patient_id, doctor_id, appointment_date):
        if patient_id in self.patients and doctor_id in self.doctors:
            new_appointment = Appointment(patient_id, doctor_id, appointment_date)
            self.appointments.append(new_appointment)
            messagebox.showinfo("Success", "Appointment scheduled successfully.")
        else:
            messagebox.showerror("Error", "Patient or Doctor ID not found.")

    def issue_prescription(self, patient_id, prescription):
        for appointment in self.appointments:
            if appointment.patient_id == patient_id and appointment.prescription is None:
                appointment.prescription = prescription
                self.prescriptions_stack.append(appointment)
                self.appointments = [appt for appt in self.appointments if appt.patient_id != patient_id]
                messagebox.showinfo("Success", f"Prescription issued for patient ID {patient_id}.")
                return
        messagebox.showerror("Error", "Appointment not found or prescription already issued.")
            def get_patient_records(self):
        sorted_patients = sorted(self.patients.values(), key=lambda x: x.admission_date)
        return sorted_patients

    def remove_patient(self, patient_id):
        if patient_id in self.patients:
            del self.patients[patient_id]
            self.appointments = [appt for appt in self.appointments if appt.patient_id != patient_id]
            messagebox.showinfo("Success", "Patient removed successfully.")
        else:
            messagebox.showerror("Error", "Patient ID not found.")

    def remove_appointment_by_patient_id(self, patient_id):
        # Find and remove the first appointment for the given patient ID
        for i, appointment in enumerate(self.appointments):
            if appointment.patient_id == patient_id:
                del self.appointments[i]
                return True
        return False

    def update_patient_record(self, patient_id, name=None, medical_condition=None, admission_date=None):
        patient = self.patients.get(patient_id)
        if patient:
            if name:
                patient.name = name
            if medical_condition:
                patient.medical_condition = medical_condition
            if admission_date:
                patient.admission_date = datetime.datetime.strptime(admission_date, "%Y-%m-%d").date()
            return True
        return False


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
