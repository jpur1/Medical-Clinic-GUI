class Note:
    def __init__(self, code, text):
        self.code = code
        self.text = text
        self.timestamp = None

    # Getters
    def get_text(self):
        return self.text

    # Setters
    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def __str__(self):
        """
        Purpose: Return a string representation of the Note object.
        Returns: str - A formatted string of the Note.
        """
        return f"Note {self.code}: '{self.text}', Timestamp: {self.timestamp})"

    def __eq__(self, other):
        """
        Purpose: Compare two Note objects for equality.
        Args:
            other (Note): The other Note object to compare.
        Returns: bool - True if equal, False otherwise.
        """
        if not isinstance(other, Note):
            return NotImplemented
        return (self.code == other.code and
                self.text == other.text)