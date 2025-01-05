#make sure code runs on python 3.9.19!!!
import hashlib
from .patient import *
from .patient_record import *
from .note import *
from datetime import datetime
from typing import List # so I can do List[] for typehints
from .dao.patient_dao_json import PatientDAOJSON

from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

class Controller:
    def __init__(self, autosave=False):
        self.users = {"user" : "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", 
                      "ali":"6394ffec21517605c1b426d43e6fa7eb0cff606ded9c2956821c2c36bfee2810", 
                      "kala":"e5268ad137eec951a48a5e5da52558c7727aaa537c8b308b5e403e6b434e036e"}
        self.logged_in_user = None
        self.current_patient = None
        self.autosave = autosave
        self.patient_dao = PatientDAOJSON(self.autosave)
       

    def load_users(self):
        with open("users.txt", "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    username, password_hash = parts
                    self.users[username] = password_hash
        return self.users

    def get_password_hash(self, password) -> str:
        """
        Purpose: Generate a secure SHA-256 hash for the password.
        Args: password (str) - password for the user's login
        Return: a string represetation of the hex digit version of password
        """
        encoded_password = password.encode('utf-8')     # Convert the password to bytes
        hash_object = hashlib.sha256(encoded_password)      # Choose a hashing algorithm (e.g., SHA-256)
        hex_dig = hash_object.hexdigest()       # Get the hexadecimal digest of the hashed password
        return hex_dig

    def login(self, username: str, password: str) -> bool:
        """"
        Purpose: The user enters username and password. The system checks the user
                 name and the password within the system and either logs in or not.
                Args: username (str) - The username of the user trying to log in.
                password (str)- The password provided by the user.
                Returns: bool, True if successful login, raises exception otherwise
        """
        if self.logged_in_user:
                raise DuplicateLoginException("User already is logged in.")
        
        password_hash = self.get_password_hash(password)
        if self.users.get(username) == password_hash:
            self.logged_in_user = username
            print(f"Login successful: Welcome {username}!")
            return True   
        else:
            raise InvalidLoginException("Invalid username or password.")

    def logout(self) -> True:
        """
        Purpose: The user logs out of the system.
        Returns: True or raises exception
        """
        if self.logged_in_user:
            self.logged_in_user = None
            print(f"Log out complete")
            return True
        else:
            raise InvalidLogoutException("No user is logged in.")

    def is_logged(self) -> None:
        """
        Purpose: Checks if a user is currently logged in.
        Returns: void
        """
        return self.logged_in_user is not None
    
    def search_patient(self, phn: int) -> Patient:
        """
        Purpose: The user searches a patient by Personal Health Number (PHN). If
                 successful, it returns the patient.
        Args: phn (int) - number representing the patient in the system.
        Returns: patient, raises exception otherwise
        """
        if not self.is_logged():
            raise IllegalAccessException("Cannot search when user is not logged in.")
        return self.patient_dao.search_patient(phn)

    def create_patient(self, phn: int, name: str, birth_date: str, 
                       phone: str, email: str, address: str) -> Patient:
        """
        Purpose: The user creates a new patient in the system, with their personal health
                 number, name and other personal data.
        Args: phn (int) - number representing the patient in the system.
              name (str) - name of patient.
              birth_date (str) - birth date of patient.
              phone (str) - phone number of patient.
              email (str) - email of patient.
              address (str) - home address of patient.
        Returns: Patient, raises exception otherwise
        """
        if not self.is_logged():
            raise IllegalAccessException("Cannot create patient without logging in.")
            
        if phn in self.patient_dao.patients:
            raise IllegalOperationException("Cannot add a patient with a phn that is already registered.")
        
        new_patient = Patient(phn, name, birth_date, phone, email, address, self.autosave)
        self.patient_dao.create_patient(new_patient)
        return new_patient

    def retrieve_patients(self, name: str) -> List[Patient]:
        """
        Purpose: The user searches the patients by name, and retrieves a list of patients
                 that have the searched name as part of the patient’s name
        Args: name (str) - name of the patient
        Returns: list of patients, or raises an exception if not logged in.
        """
        if not self.is_logged():
            raise IllegalAccessException("Cannot retrieve patients without logging in.")
        
        return self.patient_dao.retrieve_patients(name)
        
    def update_patient(self, phn: int, new_phn: int, name: str, birth_date: str, 
                       phone: str, email: str, address: str) -> Patient:
        """
        Purpose: The user searches the patient by PHN, retrieves the patient data, and
                 updates any part of that data.
        Args: phn (int) - number representing the patient in the system.
              new_phn (int) - updated phn.
              name (str) - name of patient.
              birth_date (str) - birth date of patient.
              phone (str) - phone number of patient.
              email (str) - email of patient.
              address (str) - home address of patient.
        Returns: Patient, raises exception otherwise
        """
        if not self.is_logged():
            raise IllegalAccessException("Cannot update patient without logging in.")
        
        patient = self.patient_dao.search_patient(phn)

        # Check if the current PHN exists
        if phn not in self.patient_dao.patients:
            raise IllegalOperationException("Cannot update patient with a phn that is not registered.")
        
        # Check that the new PHN doesn't conflict with existing ones
        if self.patient_dao.search_patient(new_phn) and new_phn != phn:
            raise IllegalOperationException("Cannot update patient and give them a registered phn.")
        
        # patient is current patient, cannot update
        if self.current_patient:
            if patient == self.current_patient:
                raise IllegalOperationException("Cannot update the current patient, unset current patient first.")

        #Allows for an update of each piece of information
        patient.phn = new_phn
        if name: patient.name = name
        if birth_date: patient.birth_date = birth_date
        if phone: patient.phone = phone
        if email: patient.email = email
        if address: patient.address = address

        if new_phn != phn:
            del self.patient_dao.patients[phn]
        self.patient_dao.update_patient(new_phn, patient)

        return patient

    def delete_patient(self, phn: int) -> bool:
        """
        Purpose: The user searches the patient by PHN and deletes the patient from the system
        Args: phn (int) - number representing the patient in the system.
        Return: bool - True if deleted, raises exception otherwise
        """
        if not self.is_logged():
            raise IllegalAccessException("Cannot delete patient without logging in.")
        
        patient = self.patient_dao.search_patient(phn)

        if phn not in self.patient_dao.patients:
            raise IllegalOperationException("Cannot delete patient with a phn that is not registered.")

        # patient is current patient, cannot delete
        if self.current_patient:
            if patient == self.current_patient:
                raise IllegalOperationException("Cannot delete the current patient, unset current patient first.")
        patient = self.patient_dao.search_patient(phn)
        self.patient_dao.delete_patient(phn)
        return True
        
    def list_patients(self) -> List[Patient]:
        """
        Purpose: The user recovers a list of all the patients.
        Return: list of Patients, raises exception otherwise
        """
        if not self.is_logged():
            raise IllegalAccessException("Cannot list patients without logging in.")
        
        return self.patient_dao.list_patients()
            
    def get_current_patient(self) -> Patient:
        """
        Purpose: Get the current patient
        Returns: Patient, raises exception otherwise
        """
        if not self.is_logged():
            raise IllegalAccessException("Cannot get current patient without logging in.")

        #get the current_pattient attribute from controller
        return getattr(self, 'current_patient', None)
    
    def set_current_patient(self, phn: int) -> Patient:
        """
        Purpose: The user sets the current patient by providing a valid PHN, the patient
                 is searched and made the current patient. Then, it is available to work
                 with no further need to provide a PHN.
        Args: phn (int) - number representing the patient in the system.
        Returns: Patient
        """
        if not self.is_logged():
            raise IllegalAccessException("Cannot set current patient without logging in.")
        
        if phn not in self.patient_dao.patients:
            raise IllegalOperationException("Cannot set non-existent patient as the current patient.")
       
        self.current_patient = self.patient_dao.search_patient(phn)
        return self.current_patient
    
    def unset_current_patient(self):
        """
        Purpose: Unset the current patient
        Returns: None, raise exception otherwise
        """
		# must be logged in to do operation
        if not self.is_logged():
            raise IllegalAccessException("Cannot unset current patient without logging in.")

        if not self.current_patient:
            raise IllegalOperationException("No current patient to unset.")
    
		# unset current patient
        self.current_patient = None

    def create_note(self, input: str) -> Note:
        """
        Purpose: The user creates a new note for the current patient’s record, delegating the
                 creation of the note to the patient record. The note’s code is stored as the 
                 auto-incremented counter from the patient record, along with its details and 
                 timestamp
        Args: input (str) - note that the user would like to add
        Returns: Note, raises exception otherwise
        """
        if not self.is_logged():
            raise IllegalAccessException("Cannot add note for a patient without logging in.")

        if not self.current_patient:
            raise NoCurrentPatientException("Cannot add note without a valid current patient.")

        new_note = self.current_patient.patient_record.create_note_in_record(input)

        return new_note
      
    
    def search_note(self, code: int) -> List[Note]:
        """
        Purpose: The user searches the current patient’s record by a code, and retrieves
                 a note that matches the search code. The search operation is delegated to
                 the PatientRecord.
        Args: code (int) - code to search for in records
        Returns: Note, raises exception otherwise
        """
        if not self.is_logged():
            raise IllegalAccessException("Cannot search note for a patient without logging in.")

        if not self.current_patient: 
            raise NoCurrentPatientException("Cannot search note without a valid current patient.")

        return self.current_patient.patient_record.find_note_by_code(code)  
        
    def retrieve_notes(self, search_text: str) -> List[Note]:
        """
        Purpose: The user searches the current patient’s record by text, and retrieves a
                list of notes that have the searched text inside the note. The search is 
                delegated to the PatientRecord.
        Args: search_text (str) - text to search for in records
        Returns: list of Notes, raises exception otherwise
        """
        if not self.is_logged(): 
            raise IllegalAccessException("Cannot retrieve notes for a patient without logging in.")

        if not self.current_patient:
            raise NoCurrentPatientException("Cannot retrieve notes without a valid current patient.")
        
        return self.current_patient.patient_record.find_notes_by_text(search_text)

    def update_note(self, code: int, new_input: str) -> Note:
        """
        Purpose: The user selects a note by code in the current patient’s record and updates
                the details and timestamp. The update operation is delegated to the PatientRecord.
        Args: code (int) - code of note to update
            new_input (str) - text to replace previous text
        Returns: Note, raises exception otherwise
        """
        if not self.is_logged():
            raise IllegalAccessException("Cannot update note for a patient without logging in.")
        
        if not self.current_patient: 
            raise NoCurrentPatientException("Cannot update note without a valid current patient.")

        return self.current_patient.patient_record.update_note_by_code(code, new_input)

    def delete_note(self, code: int) -> bool:
        """
        Purpose: The user selects a note by code in the current patient’s record, and deletes 
                the note. The deletion operation is delegated to the PatientRecord.
        Args: code (int) - code of note to delete
        Returns: bool - True if deleted, raises exception otherwise
        """
        if not self.is_logged():
            raise IllegalAccessException("Cannot delete note for a patient without logging in.")
        
        if not self.current_patient: 
            raise NoCurrentPatientException("Cannot delete note without a valid current patient.")

        return self.current_patient.patient_record.delete_note_by_code(code)
            
    def list_notes(self) -> List[Note]:
        """
        Purpose: The user lists the full patient record with all the notes, from the last
                created note to the first created note. The operation is delegated to the PatientRecord.
        Returns: list of Notes, or raises exception if not logged in or current patient is not selected.
        """
        if not self.is_logged():
            raise IllegalAccessException("Cannot list notes for a patient without logging in.")
            
        if not self.current_patient: 
            raise NoCurrentPatientException("cannot list notes without a valid current patient")

        return self.current_patient.patient_record.get_all_notes()
