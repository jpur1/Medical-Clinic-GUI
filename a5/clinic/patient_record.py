from datetime import datetime
from .note import Note
from typing import List # so I can do List[] for typehints
from .dao.note_dao_pickle import NoteDAOPickle

class PatientRecord:
    def __init__(self, phn, autosave):
        self.note_dao = NoteDAOPickle(phn, autosave)
        self.autosave = autosave
        
    def create_note_in_record(self, input:str) -> Note:
        """
        Purpose: Create a new note with the provided input, storing the note’s code as the
                 auto-incremented counter, and also storing the note’s details and current 
                 timestamp in the PatientRecord.
        Args: input (str) - note that the user would like to add
        Returns: Note
        """
        # adds a new note to the patient's record at the position of autocounter
        return self.note_dao.create_note(input)
  
    
    def find_note_by_code(self, code: int) -> Note:
        """
        Purpose: Search for a note with the given code in the PatientRecord.
        Args: code (int) - code to search for in records
        Returns: Note if found, None otherwise
        """
        # Go through the notes, checking for a specific note code
        return self.note_dao.search_note(code)
    
    def find_notes_by_text(self, search_text: str) -> List[Note]:
        """
        Purpose: Search for notes containing the given text (case-insensitive) in the 
                 PatientRecord.
        Args: search_text (str) - text to search for in notes
        Returns: list of matching Notes
        """
        # Delegate note retrievel to note dao
        return self.note_dao.retrieve_notes(search_text)

    def update_note_by_code(self, code: int, new_input: str) -> bool:
        """
        Purpose: Update the text and timestamp of a note with the given code in the PatientRecord.
        Args: code (int) - code of note to update
              new_input (str) - text to replace previous text
        Returns: True if found and updated, False otherwise
        """
        if not self.note_dao.notes:
            return False
    
        self.note_dao.update_note(code, new_input)
        
        return True
    
    def delete_note_by_code(self, code: int) -> bool:
        """
        Purpose: Delete a note with the given code in the PatientRecord.
        Args: code (int) - code of note to delete
        Returns: bool - True if deleted, False if the note does not exist
        """
        if code in self.note_dao.notes:
            self.note_dao.delete_note(code)
            return True
        return False

    def get_all_notes(self) -> List[Note]:
        """
        Purpose: Retrieve a list of all notes, from the last created to the first.
        Returns: list of Notes in reverse order.
        """
        return self.note_dao.list_notes()
    
    def __eq__(self, other):
        """
        Purpose: Compare two PatientRecord objects for equality.
        Args:
            other (PatientRecord): The other PatientRecord object to compare.
        Returns: bool - True if equal, False otherwise.
        """
        if not isinstance(other, PatientRecord):
            return False
        return self.counter == other.counter and self.text == other.text

    def __str__(self):
        """
        Purpose: Return a string representation of the PatientRecord object.
        Returns: str - A formatted string of the PatientRecord.
        """
        notes_str = "\n".join(str(note) for note in self.notes.values())
        return f"PatientRecord(autocounter={self.autocounter}, Notes:\n{notes_str}\n)"
    