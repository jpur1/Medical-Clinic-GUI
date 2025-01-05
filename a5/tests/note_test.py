import unittest
from datetime import datetime
from clinic.patient import Patient
from clinic.note import Note

class TestNote(unittest.TestCase):
    def setUp(self):
        self.note1 = Note(code="N001", text="Initial consultation")
        self.note2 = Note(code="N001", text="Initial consultation")
        self.note3 = Note(code="N002", text="Follow-up visit")

    def test_note_equality(self):
        # Test equality operator (__eq__)
        self.assertEqual(self.note1, self.note2, "Notes with identical data should be equal")
        self.assertNotEqual(self.note1, self.note3, "Notes with different data should not be equal")

    def test_note_string_representation(self):
        # Test string representation (__str__)
        expected_str = "Note N001: Initial consultation"
        self.assertEqual(str(self.note1), expected_str, "String representation of Note is incorrect")

if __name__ == '__main__':
    unittest.main()
