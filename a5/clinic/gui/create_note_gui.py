import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QVBoxLayout

from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

class CreateNoteGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Create Note for Patient")
        self.setGeometry(100, 100, 400, 200)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()

        # Labels created
        self.label_note= QLabel("Enter Note:")
        self.label_sub_text = QLabel("* Must have a current patient set *")
        self.label_sub_text.setStyleSheet("color: grey; font-style: italic;")
        self.text_note = QLineEdit()
        self.text_note.setPlaceholderText("Enter note here")

        # Add labels as widget to window
        layout.addWidget(self.label_note)
        layout.addWidget(self.label_sub_text)
        layout.addWidget(self.text_note)

        # Connect create button to create note method below
        self.button_create = QPushButton("Create")
        self.button_create.clicked.connect(self.create_note)

        layout.addWidget(self.button_create)

        self.label_result = QLabel("")
        layout.addWidget(self.label_result)

        main_widget.setLayout(layout)

    def create_note(self):
        """
        Purpose: Store note information, create the note on the backend, them return a success message. 
                 Otherwise, raise exceptions.
        """
        try:
            note = self.text_note.text()
            self.controller.create_note(note)
            QMessageBox.information(self, "Success", f"Patient note created successfully!")
        except NoCurrentPatientException:
            QMessageBox.warning(self, "Error", "Cannot add note without a valid current patient.")
        except IllegalAccessException:
            QMessageBox.warning(self, "Access Error", "Cannot add note for a patient without logging in.")

def main():
    from clinic.controller import Controller
    app = QApplication(sys.argv)
    controller = Controller()
    window = CreateNoteGUI(controller)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
