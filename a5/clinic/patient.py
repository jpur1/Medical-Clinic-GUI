from .patient_record import *

class Patient:
    def __init__(self, phn, name, birth_date, phone, email, address, autosave=False):
        self.phn = phn
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.address = address
        self.autosave = autosave
        self.patient_record = PatientRecord(phn, self.autosave)
    
        
    def __eq__(self, other):
        """
        Purpose: Compare two Patient objects for equality.
        Args:
            other (Patient): The other Patient object to compare.
        Returns: bool - True if equal, False otherwise.
        """
        if isinstance(other, Patient):
            return (self.phn == other.phn and
                self.name == other.name and
                self.birth_date == other.birth_date and
                self.phone == other.phone and
                self.email == other.email and
                self.address == other.address)
        return False
        
    def __str__(self):
        """
        Purpose: Return a string representation of the Patient object.
        Returns: str - A formatted string of the Patient.
        """
        return f"Patient(PHN: {self.phn}, Name: {self.name}, Birth Date: {self.birth_date}, Phone: {self.phone}, Email: {self.email}, Address: {self.address})"
    
    def __repr__(self):
        return f"Patient(PHN: {self.phn}, Name: {self.name}, DOB: {self.birth_date})"
