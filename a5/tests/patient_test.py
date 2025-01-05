import unittest
from datetime import datetime
from clinic.patient import Patient
from clinic.note import Note

class TestPatient(unittest.TestCase):
    def setUp(self):
         self.patient1 = Patient(
                phn="1234567890",
                name="John Doe",
                birth_date=datetime(1990, 1, 1),
                phone="123-456-7890",
                email="john.doe@example.com",
                address="123 Main St"
        )
         self.patient2 = Patient(
                phn="1234567890",
                name="John Doe",
                birth_date=datetime(1990, 1, 1),
                phone="123-456-7890",
                email="john.doe@example.com",
                address="123 Main St"
        )
         self.patient3 = Patient(
                phn="0987654321",
                name="Jane Smith",
                birth_date=datetime(1985, 5, 15),
                phone="987-654-3210",
                email="jane.smith@example.com",
                address="456 Elm St"
        )

    def test_patient_equality(self):
        # Test equality operator (__eq__)
        self.assertEqual(self.patient1, self.patient2, "Patients with identical data should be equal")
        self.assertNotEqual(self.patient1, self.patient3, "Patients with different data should not be equal")

    def test_patient_string_representation(self):
        # Test string representation (__str__)
        expected_str = "Patient(PHN: 1234567890, Name: John Doe, Birth Date: 1990-01-01 00:00:00)"
        self.assertEqual(str(self.patient1), expected_str, "String representation of Patient is incorrect")

if __name__ == '__main__':
    unittest.main()