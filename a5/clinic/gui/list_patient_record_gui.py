import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

from PyQt6.QtWidgets import QLabel, QPushButton, QMessageBox
from PyQt6.QtWidgets import QVBoxLayout, QPlainTextEdit

from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

class ListPatientRecordGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("List Patient Notes")
        self.setGeometry(100, 100, 625, 600)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()

        # Labels created, style a label to tell user that a current patient must be set
        self.label_sub_text = QLabel("* Must have a current patient set *")
        self.label_sub_text.setStyleSheet("color: grey; font-style: italic;")

        # Create patient to add their name to top of the record
        patient = self.controller.get_current_patient()

        if patient is None:
            self.label_title = QLabel("No patient selected")
        else:
            self.label_title = QLabel(f"Patient {patient.name}'s Notes")
       
        # Add labels as widgets to window
        layout.addWidget(self.label_sub_text)
        layout.addWidget(self.label_title)

        # QPlainTextEdit widget created, made to only be read, add to window
        self.notes_display = QPlainTextEdit()
        self.notes_display.setReadOnly(True)
        layout.addWidget(self.notes_display)

        main_widget.setLayout(layout)

        self.list_notes()

    def list_notes(self):
        """
        Purpose: Store list of notes, format in a user friendly way, then pass to be displayed.
                 Otherwise, raise exceptions.
        """
        try:
            notes = self.controller.list_notes()
            if notes:
                formatted_notes = "\n\n".join(
                    f"Note ID: {note.code}\nDate: {note.timestamp}\nContent: {note.text}"
                    for note in notes
                )
                self.notes_display.setPlainText(formatted_notes)
            else:
                self.notes_display.setPlainText("No notes available for this patient.")
        except IllegalAccessException:
            QMessageBox.warning(self, "Access Error", "Cannot list notes for a patient without logging in.")
        except NoCurrentPatientException:
            QMessageBox.warning(self, "Error", "Cannot list notes without a valid current patient")

def main():
    from clinic.controller import Controller
    app = QApplication(sys.argv)
    controller = Controller()
    window = ListPatientRecordGUI(controller)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
