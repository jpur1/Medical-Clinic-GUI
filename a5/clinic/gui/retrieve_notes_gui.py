import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QVBoxLayout, QPlainTextEdit

from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException


class RetrieveNotesGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Retrieve Existing Notes")
        self.setGeometry(100, 100, 625, 600)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()

        # Labels created, style a label to tell user that a current patient must be set
        self.label_search = QLabel("Retrieve Notes:")
        self.text_search = QLineEdit()
        self.label_sub_text = QLabel("* Must have a current patient set *")
        self.label_sub_text.setStyleSheet("color: grey; font-style: italic;")

        # Placeholder text, then connect search button to retrieve notes method below
        self.text_search.setPlaceholderText("Enter text to search for in notes")
        self.button_search = QPushButton("Search")
        self.button_search.clicked.connect(self.retrieve_notes)

        # Add labels as widgets to window
        layout.addWidget(self.label_search)
        layout.addWidget(self.label_sub_text)
        layout.addWidget(self.text_search)
        layout.addWidget(self.button_search)

        # Create a plain text editor widget to display the notes
        # Read only, add as widgets to window
        self.label_notes = QLabel("Notes Found:")
        self.text_notes = QPlainTextEdit()
        self.text_notes.setReadOnly(True)

        layout.addWidget(self.label_notes)
        layout.addWidget(self.text_notes)

        main_widget.setLayout(layout)

    def retrieve_notes(self):
        """
        Purpose: Store search input, if none tell user to input some text. Retrieve the notes,
                 format them in user friendly way, then add to display. Otherwise, say nothing
                 is found or raise exceptions.
        """
        search_text = self.text_search.text().strip()
        if not search_text:
            QMessageBox.warning(self, "Input Error", "Please enter text to search.")
            return
        
        try:
            notes = self.controller.retrieve_notes(search_text)
            if notes:
                formatted_notes = "\n\n".join(f"- {note}" for note in notes)
                self.text_notes.setPlainText(formatted_notes)
            else:
                self.text_notes.setPlainText("No notes found matching the search text.")
        except NoCurrentPatientException:
            QMessageBox.warning(self, "Error", "Cannot retrieve notes without a valid current patient.")
        except IllegalAccessException:
            QMessageBox.warning(self, "Access Error", "Cannot retrieve notes for a patient without logging in.")
   
def main():
    from clinic.controller import Controller
    app = QApplication(sys.argv)
    controller = Controller()
    window = RetrieveNotesGUI(controller)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
