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
