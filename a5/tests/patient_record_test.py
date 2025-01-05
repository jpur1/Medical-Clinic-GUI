import unittest
from clinic.patient import *
from clinic.patient_record import *
from clinic.note import *
from clinic.controller import *
from datetime import datetime

class TestPatientRecord(unittest.TestCase):
        def setUp(self):
            self.patient_record = PatientRecord()
            

            self.patient1 = Patient(
                phn="1234567890",
                name="John Doe",
                birth_date=datetime(1990, 1, 1),
                phone="123-456-7890",
                email="john.doe@example.com",
                address="123 Main St"
            )

            self.patient2 = Patient(
                phn="0987654321",
                name="Jane Smith",
                birth_date=datetime(1985, 5, 15),
                phone="987-654-3210",
                email="jane.smith@example.com",
                address="456 Elm St"
            )
            self.note1 = Note(code="N001", text="Initial consultation")
            self.note2 = Note(code="N002", text="Follow-up visit")

            self.patient_record.notes[self.patient1.phn] = self.note1
            self.patient_record.notes[self.patient2.phn] = self.note2

        def test_patient_record_equality(self):
            # Tests equality operator (__eq__)
            patient_record2 = PatientRecord()
            patient_record2.notes[self.patient1.phn] = self.note1
            patient_record2.notes[self.patient2.phn] = self.note2

            self.assertEqual(self.patient_record, patient_record2, "PatientRecord instances with identical data should be equal")

            # Modify patient_record2 to make them different
            patient_record2.autocounter = 2
            self.assertNotEqual(self.patient_record, patient_record2, "PatientRecord instances with different autocounters should not be equal")

        def test_patient_record_string_representation(self):
            # Test string representation (__str__)
            expected_str = (
                f"PatientRecord(autocounter={self.patient_record.autocounter}, Notes:\n"
                f"{self.note1}\n"
                f"{self.note2}\n)"
            )
            self.assertEqual(str(self.patient_record), expected_str, "String representation of PatientRecord is incorrect")

        def test_empty_patient_record_equality(self):
            empty_patient_record = PatientRecord()
            self.assertNotEqual(self.patient_record, empty_patient_record, "Two empty PatientRecord instances should not be equal")

        def test_adding_duplicate_note(self):
            self.patient_record.notes[self.patient1.phn] = Note(code="N003", text="Updated note")
            expected_str = (
                f"PatientRecord(autocounter={self.patient_record.autocounter}, Notes:\n"
                f"{Note(code='N003', text='Updated note')}\n"
                f"{self.note2}\n)"
            )
            self.assertEqual(str(self.patient_record), expected_str, "String representation should reflect the updated note")


        def test_create_note_in_record(self):
            """Test creating a new note in the record."""
            note_text = "This is a test note."
            note = self.patient_record.create_note_in_record(note_text)
            
            # Check if the note was created correctly
            self.assertIsNotNone(note)
            self.assertEqual(note.code, 1)
            self.assertEqual(note.get_text(), note_text)
            self.assertIsInstance(note.timestamp, datetime)
            
            # Ensure that the note was added to the record
            self.assertIn(1, self.patient_record.notes)
            self.assertEqual(self.patient_record.notes[1], note)

        def test_find_note_by_code(self):
            """Test finding a note by its code."""
            # Create a note and search for it
            note_text = "Another test note."
            self.patient_record.create_note_in_record(note_text)
            
            note = self.patient_record.find_note_by_code(1)
            
            # Check if the note was found
            self.assertEqual(note.code, 1)
            self.assertEqual(note.get_text(), note_text)
            
            # Check for a non-existent note
            self.assertIsNone(self.patient_record.find_note_by_code(999))

        def test_find_notes_by_text(self):
            """Test searching for notes by text (case-insensitive)."""
            # Create several notes
            self.patient_record.create_note_in_record("First Note")
            self.patient_record.create_note_in_record("Second Note")
            self.patient_record.create_note_in_record("Another note")
            
            # Search for notes containing "note" (case-insensitive)
            results = self.patient_record.find_notes_by_text("note")
            self.assertEqual(len(results), 3)
            
            # Search for notes containing "first"
            results = self.patient_record.find_notes_by_text("first")
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].get_text(), "First Note")

            # Search for text not present
            results = self.patient_record.find_notes_by_text("not found")
            self.assertEqual(len(results), 0)

        def test_update_note_by_code(self):
            """Test updating a note by its code."""
            # Create a note
            self.patient_record.create_note_in_record("Initial note")
            
            # Update the note's text
            updated_text = "Updated note content"
            updated_note = self.patient_record.update_note_by_code(1, updated_text)
            
            # Check if the update was successful
            self.assertEqual(updated_note.code, 1)
            self.assertEqual(updated_note.get_text(), updated_text)
            self.assertIsInstance(updated_note.timestamp, datetime)
            
            # Check if the note was updated in the record
            note = self.patient_record.find_note_by_code(1)
            self.assertEqual(note.get_text(), updated_text)

            # Try updating a non-existent note
            self.assertIsNone(self.patient_record.update_note_by_code(999, "No change"))

        def test_delete_note_by_code(self):
            """Test deleting a note by its code."""
            # Create a note
            self.patient_record.create_note_in_record("To be deleted")
            
            # Delete the note
            deleted = self.patient_record.delete_note_by_code(1)
            self.assertTrue(deleted)
            
            # Ensure the note is no longer in the record
            self.assertIsNone(self.patient_record.find_note_by_code(1))
            self.assertFalse(self.patient_record.delete_note_by_code(1))  # Attempt to delete again

        def test_get_all_notes(self):
            """Test retrieving all notes in reverse order."""
            # Create several notes
            self.patient_record.create_note_in_record("First")
            self.patient_record.create_note_in_record("Second")
            self.patient_record.create_note_in_record("Third")
            
            # Retrieve notes in reverse order
            notes = self.patient_record.get_all_notes()
            
            # Ensure the order is correct (last created to first)
            self.assertEqual(len(notes), 5)
            self.assertEqual(notes[0].get_text(), "Third")
            self.assertEqual(notes[1].get_text(), "Second")
            self.assertEqual(notes[2].get_text(), "First")

if __name__ == '__main__':
    unittest.main()