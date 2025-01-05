import pickle
from .note_dao import NoteDAO
from clinic.note import Note
from datetime import datetime
from typing import List # so I can do List[] for typehints


class NoteDAOPickle(NoteDAO):
    def __init__(self, phn, autosave):
        self.notes = {}
        self.counter = 0
        self.autosave = autosave
        self.filename = f'clinic/records/{phn}.dat'
        self.load_notes()

    def load_notes(self) -> None:
        """
        Purpose: Loads notes from the pickle file into the notes dictionary. 
                 Updates the counter to the highest note code.
        """
        if self.autosave:
            try:
                with open(self.filename, 'rb') as file:
                    self.notes = pickle.load(file)
                    if self.notes:
                        temp_notes = list(self.notes.values())
                        self.counter = temp_notes[-1].code
            except FileNotFoundError:
                self.notes = {}
        else:
            self.notes = {}

    def save_notes(self) -> None:
        """
        Purpose: Saves the current notes dictionary to the pickle file.
        """
        with open(self.filename, "wb") as file:
            pickle.dump(self.notes, file)

    def search_note(self, key: int) -> Note:
        """
        Purpose: : Search for a note by its unique key (code).
        Args: key (int) - the unique identifier (code) of the note to search for
        Return: the note object if found, None otherwise
        """
        note = self.notes.get(key)
        if note:
            return note
        return None
         
    def create_note(self, text: str) -> Note:
        """
        Purpose: Create a new note with the given text, assign it a unique code, and add it to the notes dictionary.
        Args: text (str) - text to input into new note
        Return: Note
        """
        self.counter += 1

        note = Note(self.counter, text)
        timestamp = datetime.now()
        note.set_timestamp(timestamp)
        self.notes[note.code] = note

        if self.autosave:
            self.save_notes()
        
        return note
    
    def retrieve_notes(self, search_string: str) -> List[Note]:
        """
        Purpose: Retrieve all notes that contain a specific search string in their text (case-insensitive).
        Args: search_string (str) - the text to search for within the notes
        Return: list of notes
        """
        return [note for note in self.notes.values() if search_string.lower() in note.get_text().lower()]

    def update_note(self, key: int, text: str) -> bool:
        """
        Purpose: Update the text of a note identified by its key and set a new timestamp.
        Args: key (int) - the unique identifier (code) of the note to search for
              text (str) - text to input into new note
        Return: True if successfully updated
        """
        note = self.search_note(key)
        note.text = text
        note.set_timestamp(datetime.now())
        
        if self.autosave:
            self.save_notes()
        return True

    def delete_note(self, key: int) -> None:
        """
        Purpose: Delete a note identified by its unique note_id from the notes dictionary.
        Args: key (int) - the unique identifier (code) of the note to search for
        Return: None
        """
        if key in self.notes:
            del self.notes[key]
            if self.autosave:
                self.save_notes()

    def list_notes(self) -> List[Note]:
        """
        Purpose: List all notes in reverse order of their creation (most recent first).
        Return: a reversed list of Notes
        """
        return list(reversed(self.notes.values()))
    