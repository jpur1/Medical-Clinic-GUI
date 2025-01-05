import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QVBoxLayout

from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

class UpdateNoteGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Update Note")
        self.setGeometry(100, 100, 300, 300)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()

        # Labels created, style a label to tell user that a current patient must be set
        self.label_sub_text = QLabel("* Must have a current patient set *")
        self.label_sub_text.setStyleSheet("color: grey; font-style: italic;")

        self.label_code = QLabel("Enter Note Code:")
        self.text_code = QLineEdit()
        self.text_code.setPlaceholderText("Note code")

        self.label_new_note = QLabel("Enter New Details:")
        self.text_new_note = QLineEdit()
        self.text_new_note.setPlaceholderText("Update the note here")

        # Labels added as widgets to window
        layout.addWidget(self.label_sub_text)
        layout.addWidget(self.label_code)
        layout.addWidget(self.text_code)
        layout.addWidget(self.label_new_note)
        layout.addWidget(self.text_new_note)

        # Connect update button to update note method below
        self.button_update = QPushButton("Update")
        self.button_update.clicked.connect(self.update_note)

        layout.addWidget(self.button_update)

        self.label_result = QLabel("")
        layout.addWidget(self.label_result)

        main_widget.setLayout(layout)

    def update_note(self):
        """
        Purpose: Store code and new npte, then update note from controller. Display the updated note.
                 Also, send a success message. Otherwise, raise exceptions.
        """
        try:
            code = int(self.text_code.text().strip())
            new_note = self.text_new_note.text()

            self.controller.update_note(code, new_note)
            Note = self.controller.search_note(code)
            self.label_result.setText(f"Updated Note: {Note}")

            QMessageBox.information(self, "Success", f"Note updated successfully!")

        except ValueError:
            QMessageBox.warning(self, "Value Error", "Invalid input, try again.")
        except NoCurrentPatientException:
            QMessageBox.warning(self, "Error", "Cannot update note without a valid current patient.")
        except IllegalAccessException:
            QMessageBox.warning(self, "Access Error", "Cannot update note for a patient without logging in.")

def main():
    from clinic.controller import Controller
    app = QApplication(sys.argv)
    controller = Controller()
    window = UpdateNoteGUI(controller)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
