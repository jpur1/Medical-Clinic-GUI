import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QVBoxLayout

from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException

class CreatePatientGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Create New Patient")

        layout = QVBoxLayout()

        # Add labels
        self.label_phn = QLabel("Patient Health Number (PHN):")
        self.text_phn = QLineEdit()

        self.label_name = QLabel("Name:")
        self.text_name = QLineEdit()
        
        self.label_birth_date = QLabel("Birth Date (YYYY-MM-DD):")
        self.text_birth_date = QLineEdit()

        self.label_phone = QLabel("Phone:")
        self.text_phone = QLineEdit()

        self.label_email = QLabel("Email:")
        self.text_email = QLineEdit()

        self.label_address = QLabel("Address:")
        self.text_address = QLineEdit()

        self.submit_button = QPushButton("Create Patient")
        self.cancel_button = QPushButton("Cancel")

        # Labels added as widgets to window
        layout.addWidget(self.label_phn)
        layout.addWidget(self.text_phn)
        layout.addWidget(self.label_name)
        layout.addWidget(self.text_name)
        layout.addWidget(self.label_birth_date)
        layout.addWidget(self.text_birth_date)
        layout.addWidget(self.label_phone)
        layout.addWidget(self.text_phone)
        layout.addWidget(self.label_email)
        layout.addWidget(self.text_email)
        layout.addWidget(self.label_address)
        layout.addWidget(self.text_address)

        # Add buttons
        layout.addWidget(self.submit_button)
        layout.addWidget(self.cancel_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Connect buttons to new_patient method or to close window
        self.submit_button.clicked.connect(self.new_patient)
        self.cancel_button.clicked.connect(self.close)
        
    def new_patient(self):
        """
        Purpose: Store values entered and put them into create patient method from controller.
                 Send success message, otherwise raise exceptions.
        """
        try:
            phn = int(self.text_phn.text())
            name = self.text_name.text()
            birth_date = self.text_birth_date.text()
            phone = self.text_phone.text()
            email = self.text_email.text()
            address = self.text_address.text()

            self.controller.create_patient(phn, name, birth_date, phone, email, address)

            QMessageBox.information(self, "Success", f"Patient {name} created successfully!")
            self.close()

        except ValueError:
            QMessageBox.warning(self, "Value Error", "Invalid input, please try again.")
        except IllegalOperationException:
            QMessageBox.warning(self, "Operation Error", 
                                "Cannot add a patient with a phn that is already registered.")
        except IllegalAccessException:
           QMessageBox.warning(self, "Access Error", "Cannot create patient without logging in.")
           
def main():
    from clinic.controller import Controller
    app = QApplication(sys.argv)
    controller = Controller()
    window = CreatePatientGUI(controller)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()