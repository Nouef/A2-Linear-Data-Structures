import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Label, Entry, Button, Listbox
import datetime
from collections import deque

class Patient:
    def __init__(self, patient_id, name, medical_condition, admission_date):
        self.patient_id = patient_id
        self.name = name
        self.medical_condition = medical_condition
        self.admission_date = datetime.datetime.strptime(admission_date, "%Y-%m-%d").date()

class Doctor:
    def __init__(self, doctor_id, name, specialization):
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization

class Appointment:
    def __init__(self, patient_id, doctor_id, appointment_date):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = datetime.datetime.strptime(appointment_date, "%Y-%m-%d").date()
        self.prescription = None

class HospitalSystem:
    def __init__(self):
        self.patients = {}
        self.doctors = {1: Doctor(1, "Dr. Jamal", "Cardiology"), 2: Doctor(2, "Dr. Ray", "Neurology"), 3: Doctor(3, "Dr. Wilson", "General Medicine")}
        self.appointments = deque()  # Using a deque as a queue for appointments
        self.prescriptions_stack = []  # Using a list as a stack for prescriptions
        self.add_initial_data()

    def add_initial_data(self):
        initial_patients = [
            ("Sara", "Flu", "2023-04-01", 1, "2023-04-02"),
            ("Ahmed", "Cold", "2024-04-01", 2, "2024-04-03"),
            ("Ali", "Fever", "2024-04-02", 3, "2024-04-03"),
            ("Diana", "Injury", "2024-04-02", 1, "2024-04-04"),
            ("Ethan", "Checkup", "2024-04-03", 2, "2024-04-05"),
        ]
        for name, condition, admission_date, doctor_id, appointment_date in initial_patients:
            patient_id = self.add_patient(name, condition, admission_date)
            self.schedule_appointment(patient_id, doctor_id, appointment_date)

    def consult_next_patient(self, doctor_id):
        for i, appt in enumerate(self.appointments):
            if appt.doctor_id == doctor_id and appt.prescription is None:
                return self.appointments.pop(i)
        return None

    def add_patient(self, name, condition, admission_date):
        patient_id = max(self.patients.keys(), default=0) + 1
        self.patients[patient_id] = Patient(patient_id, name, condition, admission_date)
        return patient_id
    def schedule_appointment(self, patient_id, doctor_id, appointment_date):
        if patient_id in self.patients and doctor_id in self.doctors:
            new_appointment = Appointment(patient_id, doctor_id, appointment_date)
            self.appointments.append(new_appointment)
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


class LoginSystem:
    def __init__(self):
        self.users = {"doctor1": "pass", "doctor2": "pass", "doctor3": "pass", "reception": "pass"}

    def verify_user(self, username, password):
        return self.users.get(username) == password

class HospitalSystemGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Hospital Management System")
        self.hospital_system = HospitalSystem()
        self.login_system = LoginSystem()
        self.current_user = None
        self.create_login_window()


    def create_login_window(self):
        self.clear_window()
        tk.Label(self.master, text="Username:").pack()
        username_entry = tk.Entry(self.master)
        username_entry.pack()

        tk.Label(self.master, text="Password:").pack()
        password_entry = tk.Entry(self.master, show="*")
        password_entry.pack()

        tk.Button(self.master, text="Login", command=lambda: self.login(username_entry.get(), password_entry.get())).pack()

    def login(self, username, password):
        if self.login_system.verify_user(username, password):
            self.current_user = username
            self.create_main_window()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")

    def create_main_window(self):
        self.clear_window()
        if "doctor" in self.current_user:
            self.doctor_view()
        else:
            self.receptionist_view()

    def doctor_view(self):
        self.clear_window()
        doctor_id = int(self.current_user[-1])
        tk.Label(self.master, text=f"Doctor {doctor_id}'s Patients:").pack()
        tk.Button(self.master, text="Consult Next Patient", command=self.consult_next_patient).pack()
        tk.Button(self.master, text="View Prescriptions Record", command=self.view_prescriptions_record).pack()
        tk.Button(self.master, text="Update Patient Details", command=self.update_patient_window).pack()
        tk.Button(self.master, text="Back to Login", command=self.create_login_window).pack()

    def consult_next_patient(self):
        if self.hospital_system.appointments:
            next_appointment = self.hospital_system.appointments.popleft()
            patient = self.hospital_system.patients[next_appointment.patient_id]  # Retrieve the patient object
            prescription = simpledialog.askstring("Prescription", f"Enter {patient.name}'s prescription:")
            if prescription:
                next_appointment.prescription = prescription
                self.hospital_system.prescriptions_stack.append(next_appointment)
                messagebox.showinfo("Consultation", f"{patient.name} consulted and prescription added.")
            else:
                messagebox.showinfo("Consultation", "No prescription provided. Patient requeued.")
                self.hospital_system.appointments.appendleft(next_appointment)  # Requeue if no prescription
        else:
            messagebox.showinfo("Queue Empty", "No more patients in the queue.")
        self.doctor_view()  # Refresh the view

    def view_prescriptions_record(self):
        prescriptions_win = Toplevel(self.master)
        prescriptions_win.title("Prescriptions Record")
        for appt in reversed(self.hospital_system.prescriptions_stack):  # Use reversed to mimic stack behavior
            patient = self.hospital_system.patients[appt.patient_id]
            Label(prescriptions_win, text=f"Patient: {patient.name}, Prescription: {appt.prescription}").pack()
    def consult_patient(self, appointment):
        prescription = simpledialog.askstring("Prescription", f"Enter prescription for patient ID {appointment.patient_id}:")
        if prescription:
            appointment.prescription = prescription
            self.hospital_system.prescriptions_stack.append(appointment)
            self.hospital_system.appointments.remove(appointment)
            messagebox.showinfo("Success", "Prescription added and patient removed from queue.")
            self.doctor_view()

    def receptionist_view(self):
        self.clear_window()
        tk.Button(self.master, text="Add New Patient", command=self.add_patient_window).pack()
        tk.Button(self.master, text="Remove Patient", command=self.remove_patient_window).pack()
        tk.Button(self.master, text="Update Patient Details", command=self.update_patient_window).pack()
        tk.Button(self.master, text="Schedule Appointment", command=self.schedule_appointment_window).pack()
        tk.Button(self.master, text="View Patient Records", command=self.view_patient_records).pack()
        tk.Button(self.master, text="View Appointments Queue", command=self.view_appointments_queue).pack()
        tk.Button(self.master, text="Back to Login", command=self.create_login_window).pack(side=tk.BOTTOM)

    def add_patient_window(self):
        add_win = tk.Toplevel(self.master)
        add_win.title("Add New Patient")

        tk.Label(add_win, text="Name:").grid(row=0, column=0)
        name_entry = tk.Entry(add_win)
        name_entry.grid(row=0, column=1)

        tk.Label(add_win, text="Medical Condition:").grid(row=1, column=0)
        condition_entry = tk.Entry(add_win)
        condition_entry.grid(row=1, column=1)

        tk.Label(add_win, text="Admission Date (YYYY-MM-DD):").grid(row=2, column=0)
        admission_date_entry = tk.Entry(add_win)
        admission_date_entry.grid(row=2, column=1)

        tk.Button(add_win, text="Submit", command=lambda: self.submit_new_patient(
            name_entry.get(), condition_entry.get(), admission_date_entry.get(), add_win
        )).grid(row=3, column=0, columnspan=2)

    def submit_new_patient(self, name, condition, admission_date, window):
        try:
            self.hospital_system.add_patient(name, condition, admission_date)
            window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def schedule_appointment_window(self):
        appt_win = Toplevel(self.master)
        appt_win.title("Schedule Appointment")
        Label(appt_win, text="Patient ID:").grid(row=0, column=0)
        patient_id_entry = Entry(appt_win)
        patient_id_entry.grid(row=0, column=1)
        Label(appt_win, text="Doctor ID:").grid(row=1, column=0)
        doctor_id_entry = Entry(appt_win)
        doctor_id_entry.grid(row=1, column=1)
        Label(appt_win, text="Appointment Date (YYYY-MM-DD):").grid(row=2, column=0)
        appointment_date_entry = Entry(appt_win)
        appointment_date_entry.grid(row=2, column=1)
        Button(appt_win, text="Schedule",
               command=lambda: self.schedule_appointment(patient_id_entry.get(), doctor_id_entry.get(),
                                                         appointment_date_entry.get(), appt_win)).grid(row=3, column=0,
                                                                                                       columnspan=2)

    def schedule_appointment(self, patient_id_str, doctor_id_str, appointment_date, window):
        try:
            patient_id = int(patient_id_str)
            doctor_id = int(doctor_id_str)
            if patient_id in self.hospital_system.patients:
                self.hospital_system.schedule_appointment(patient_id, doctor_id, appointment_date)
                messagebox.showinfo("Success", "Appointment scheduled successfully.", parent=window)
                window.destroy()
            else:
                messagebox.showerror("Error", "Patient ID does not exist.", parent=window)
        except ValueError as e:
            messagebox.showerror("Error", "Invalid input: " + str(e), parent=window)

    def remove_patient_window(self):
        remove_win = Toplevel(self.master)
        remove_win.title("Remove Patient")
        Label(remove_win, text="Patient ID:").grid(row=0, column=0)
        patient_id_entry = Entry(remove_win)
        patient_id_entry.grid(row=0, column=1)
        Button(remove_win, text="Remove",
               command=lambda: self.attempt_remove_patient(patient_id_entry.get(), remove_win)).grid(row=1, column=0,
                                                                                                     columnspan=2)

    def update_patient_window(self):
        update_win = Toplevel(self.master)
        update_win.title("Update Patient Record")

        Label(update_win, text="Patient ID:").grid(row=0, column=0)
        patient_id_entry = Entry(update_win)
        patient_id_entry.grid(row=0, column=1)

        Label(update_win, text="New Name:").grid(row=1, column=0)
        name_entry = Entry(update_win)
        name_entry.grid(row=1, column=1)

        Label(update_win, text="New Condition:").grid(row=2, column=0)
        condition_entry = Entry(update_win)
        condition_entry.grid(row=2, column=1)

        Label(update_win, text="New Admission Date (YYYY-MM-DD):").grid(row=3, column=0)
        admission_date_entry = Entry(update_win)
        admission_date_entry.grid(row=3, column=1)

        Button(update_win, text="Update", command=lambda: self.submit_patient_update(
            patient_id_entry.get(), name_entry.get(), condition_entry.get(), admission_date_entry.get())).grid(row=4,
                                                                                                               column=0,
                                                                                                               columnspan=2)

    def submit_patient_update(self, patient_id, name, condition, admission_date):
        updated = self.hospital_system.update_patient_record(int(patient_id), name if name else None,
                                                             condition if condition else None,
                                                             admission_date if admission_date else None)
        if updated:
            messagebox.showinfo("Success", "Patient record updated successfully.")
        else:
            messagebox.showerror("Error", "Failed to update patient record.")


    def attempt_remove_patient(self, patient_id_str, window):
        try:
            patient_id = int(patient_id_str)
            removed = self.hospital_system.remove_appointment_by_patient_id(patient_id)
            if removed:
                messagebox.showinfo("Success", "Patient removed from the appointment queue successfully.",
                                    parent=window)
            else:
                messagebox.showerror("Error", "Appointment for the given patient ID not found.", parent=window)
            window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid patient ID.", parent=window)

    def view_patient_records(self):
        records_win = Toplevel(self.master)
        records_win.title("Patient Records")
        patients_sorted_by_admission = sorted(self.hospital_system.patients.values(), key=lambda x: x.admission_date)
        for patient in patients_sorted_by_admission:
            Label(records_win,
                  text=f"ID: {patient.patient_id}, Name: {patient.name}, Condition: {patient.medical_condition}, Admission Date: {patient.admission_date}").pack()

    def view_appointments_queue(self):
        queue_win = Toplevel(self.master)
        queue_win.title("Appointments Queue")
        Label(queue_win, text="All Appointments:").pack()
        for appt in sorted(self.hospital_system.appointments, key=lambda x: x.appointment_date):
            patient = self.hospital_system.patients[appt.patient_id]
            doctor = self.hospital_system.doctors[appt.doctor_id]
            Label(queue_win,
                  text=f"Patient ID: {appt.patient_id}, Name: {patient.name}, Doctor: {doctor.name}, Date: {appt.appointment_date}").pack()
    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = HospitalSystemGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

