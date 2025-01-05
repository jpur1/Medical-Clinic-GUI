import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QVBoxLayout

from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException

class DeletePatientGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Remove Patient")
        self.setGeometry(100, 100, 400, 200)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()

        # Labels created
        self.label_phn = QLabel("Enter PHN:")
        self.text_phn = QLineEdit()
        self.text_phn.setPlaceholderText("Personal Health Number")

        # Labels added as widget to window
        layout.addWidget(self.label_phn)
        layout.addWidget(self.text_phn)

        # Delete button connected to delete patient method below
        self.button_delete = QPushButton("Delete")
        self.button_delete.clicked.connect(self.delete_patient)

        layout.addWidget(self.button_delete)

        self.label_result = QLabel("")
        layout.addWidget(self.label_result)

        main_widget.setLayout(layout)
        
    def delete_patient(self):
        """
        Purpose: Store phn and pass to delete patient in controller. Send success message, then close.
                 Otherwise, raise an exception.
        """
        try:
            phn = int(self.text_phn.text().strip())
            self.controller.delete_patient(phn)
            QMessageBox.information(self, "Success", f"Patient deleted successfully.")
            self.close()

        except ValueError:
            QMessageBox.warning(self, "Value Error", "Invalid input, try again.")
        except IllegalAccessException:
            QMessageBox.warning(self, "Access Error", "Cannot delete when user is not logged in.")
        except IllegalOperationException:
            QMessageBox.warning(self, "Operation Error", "Cannot delete patient when phn doesn't exist")

def main():
    from clinic.controller import Controller
    app = QApplication(sys.argv)
    controller = Controller()
    window = DeletePatientGUI(controller)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
