from .patient_dao import PatientDAO
import json
from .patient_decoder import PatientDecoder
from .patient_encoder import PatientEncoder
from clinic.patient import Patient # also imported for typehints
from typing import List # so I can do List[] for typehints

class PatientDAOJSON(PatientDAO):
    def __init__(self, autosave):
        self.patients = {}
        self.autosave = autosave
        self.filename = 'clinic/patients.json' 
        self.load_patients()

    def load_patients(self) -> None:
        """
        Purpose: Load patients from the specified JSON file into memory.
        Return: None
        """
        try:
            with open(self.filename, 'r') as file:
                patients_list = json.load(file, cls=PatientDecoder)
                self.patients = {patient.phn: patient for patient in patients_list}

                print(f"Loaded {len(self.patients)} patients from {self.filename}.")
                    
        except FileNotFoundError:
            print(f"{self.filename} not found. Starting with an empty patient list.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON in {self.filename}. Starting with an empty patient list.")

    def save_patients(self) -> None:
        """
        Purpose:  Save patient data to the JSON file if autosave is enabled.
        Return: None
        """
        if self.autosave:
            with open(self.filename, 'w') as file:
                patients_list = list(self.patients.values())
                json.dump(patients_list, file, cls=PatientEncoder, indent=4)

    def search_patient(self, key: int) -> Patient:
        """
        Purpose:  Search for a patient in the system by their PHN.
        Args: key (int) - the PHN for patient
        Return: Patient, or None if nothing is found.
        """
        if self.autosave:
            self.load_patients()
        return self.patients.get(key)
    
    def create_patient(self, patient: Patient) -> Patient:
        """
        Purpose: Add a new patient to the system.
        Args: patient (Patient) - the patient object to be added
        Return: Patient
        """
        self.patients[patient.phn] = patient
        if self.autosave:
            self.save_patients()
        return patient

    def retrieve_patients(self, search_string: str) -> List[Patient]:
        """
        Purpose:  Retrieve all patients whose names contain the given search string.
        Args: search_string (str): A string to search for within patient names
        Return: list of Patients
        """
        return [patient for patient in self.patients.values() if search_string.lower() in patient.name.lower()]

    def update_patient(self, key: int, patient: Patient) -> None:
        """
        Purpose: Update an existing patient's information in the system.
        Args: key (int) - the PHN for patient
              patient (Patient) - a patient object
        Return: None
        """
        self.patients[key] = patient
        if self.autosave:
            self.save_patients()

    def delete_patient(self, key: int) -> None:
        """
        Purpose: Remove a patient from the system by their unique key.
        Args: key (int) - the PHN for patient
        Return: None
        """
        if key in self.patients:
            del self.patients[key]
        if self.autosave:
            self.save_patients()

    def list_patients(self) -> List[Patient]:
        """
        Purpose: Retrieve a list of all patients in the system.
        Return: reversed list of Patients
        """
        if self.autosave:
            self.load_patients
        
        return list(self.patients.values())
    
        
