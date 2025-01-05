import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QVBoxLayout

from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException

class UpdatePatientGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Update Patient")
        self.setGeometry(100, 100, 800, 800)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()

        # Create labels for information to be updated
        self.label_phn = QLabel("Enter PHN:")
        self.text_phn = QLineEdit()
        self.text_phn.setPlaceholderText("0000000000")

        self.label_new_phn = QLabel("Enter New PHN:")
        self.text_new_phn = QLineEdit()
        self.text_new_phn.setPlaceholderText("0000000000")

        self.label_name = QLabel("Enter New Name:")
        self.text_name = QLineEdit()
        self.text_name.setPlaceholderText("John Doe")

        self.label_birth = QLabel("Enter New Birth Date:")
        self.text_birth = QLineEdit()
        self.text_birth.setPlaceholderText("YYYY-MM-DD")

        self.label_phone = QLabel("Enter New Phone:")
        self.text_phone = QLineEdit()
        self.text_phone.setPlaceholderText("012 345 6789")

        self.label_email = QLabel("Enter New Email:")
        self.text_email = QLineEdit()
        self.text_email.setPlaceholderText("johndoe@gmail.com")

        self.label_address = QLabel("Enter New Address:")
        self.text_address= QLineEdit()
        self.text_address.setPlaceholderText("Address")

        # Add labels as widgets to window
        layout.addWidget(self.label_phn)
        layout.addWidget(self.label_phn)
        layout.addWidget(self.text_phn)
        layout.addWidget(self.label_new_phn)
        layout.addWidget(self.text_new_phn)
        layout.addWidget(self.label_name)
        layout.addWidget(self.text_name)
        layout.addWidget(self.label_birth)
        layout.addWidget(self.text_birth)
        layout.addWidget(self.label_phone)
        layout.addWidget(self.text_phone)
        layout.addWidget(self.label_email)
        layout.addWidget(self.text_email)
        layout.addWidget(self.label_address)
        layout.addWidget(self.text_address)

        # Connect update button to update patient method below
        self.button_update = QPushButton("Update")
        self.button_update.clicked.connect(self.update_patient)

        layout.addWidget(self.button_update)

        self.label_result = QLabel("")
        layout.addWidget(self.label_result)

        main_widget.setLayout(layout)

    def update_patient(self):
        """
        Purpose: Store information provided, pass to controller to be updated. Then, display the
                 newly updated patient. Send a success message. Otherwise, raise exceptions.
        """
        try:
            phn = int(self.text_phn.text().strip())
            new_phn = int(self.text_new_phn.text().strip())
            name = self.text_name.text()
            birth_date = self.text_birth.text()
            phone = self.text_phone.text()
            email = self.text_email.text()
            address = self.text_address.text()

            self.controller.update_patient(phn, new_phn, name, birth_date, phone, email, address)
            patient = self.controller.search_patient(new_phn)
            self.label_result.setText(f"Updated Patient: {patient}")

            QMessageBox.information(self, "Success", f"Patient {name} updated successfully!")
          
        except ValueError:
            QMessageBox.warning(self, "Value Error", "Invalid input, try again.")
        except IllegalOperationException:
            QMessageBox.warning(self, "Operation Error", "Cannot use a PHN that is already in the system")
        except IllegalAccessException:
            QMessageBox.warning(self, "Access Error", "Cannot update when user is not logged in.")

def main():
    from clinic.controller import Controller
    app = QApplication(sys.argv)
    controller = Controller()
    window = UpdatePatientGUI(controller)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
