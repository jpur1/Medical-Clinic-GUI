import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QVBoxLayout

from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

class DeleteNoteGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Delete Note")
        self.setGeometry(100, 100, 400, 200)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()

        # Labels created, style a label to tell user that a current patient must be set
        self.label_sub_text = QLabel("* Must have a current patient set *")
        self.label_sub_text.setStyleSheet("color: grey; font-style: italic;")

        self.label_code = QLabel("Enter Note Code:")
        self.text_code = QLineEdit()
        self.text_code.setPlaceholderText("Note code")

        # Labels added as widgets to window
        layout.addWidget(self.label_sub_text)
        layout.addWidget(self.label_code)
        layout.addWidget(self.text_code)

        # Connect button to delete note method below
        self.button_delete = QPushButton("Delete")
        self.button_delete.clicked.connect(self.delete_note)

        layout.addWidget(self.button_delete)

        self.label_result = QLabel("")
        layout.addWidget(self.label_result)

        main_widget.setLayout(layout)
        
    def delete_note(self):
        """
        Purpose: Store note code, pass to delete note in controller. Send a success message, then close.
                 Otherwise, raise exceptions.
        """
        try:
            code = int(self.text_code.text().strip())
            self.controller.delete_note(code)
            QMessageBox.information(self, "Success", f"Note deleted successfully.")
            self.close()
        except ValueError:
            QMessageBox.warning(self, "Value Error", "Invalid input, try again.")
        except NoCurrentPatientException:
            QMessageBox.warning(self, "Error", "Cannot delete note without a valid current patient.")
        except IllegalAccessException:
            QMessageBox.warning(self, "Access Error", "Cannot delete note for a patient without logging in.")
        
def main():
    from clinic.controller import Controller
    app = QApplication(sys.argv)
    controller = Controller()
    window = DeleteNoteGUI(controller)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()