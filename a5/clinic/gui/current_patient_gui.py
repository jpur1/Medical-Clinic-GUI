import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QVBoxLayout

from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException

class CurrentPatientGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Set Current Patient")
        self.setGeometry(100, 100, 400, 200)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()

        # Create labels
        self.label_phn = QLabel("Enter PHN:")
        self.text_phn = QLineEdit()
        self.text_phn.setPlaceholderText("Personal Health Number")

        # Labels added as a widget to window
        layout.addWidget(self.label_phn)
        layout.addWidget(self.text_phn)

        # Connect button to set patient method below
        self.button_set = QPushButton("Set Patient")
        self.button_set.clicked.connect(self.set_patient)

        layout.addWidget(self.button_set)

        self.label_result = QLabel("")
        layout.addWidget(self.label_result)

        main_widget.setLayout(layout)

    def set_patient(self):
        """
        Purpose: Store phn, then send to set patient in controller. When succesful, display current patient.
                 Otherwise, raise exceptions.
        """
        try:
            phn = int(self.text_phn.text().strip())
            self.controller.set_current_patient(phn)
            patient = self.controller.search_patient(phn)
            self.label_result.setText(f"Current Patient:\n{patient}")
        except IllegalAccessException:
            QMessageBox.warning(self, "Access Error", "Cannot set current patient without logging in.")
        except IllegalOperationException:
            QMessageBox.warning(self, "Operation Error", "Cannot set non-existent patient as the current patient.")

def main():
    from clinic.controller import Controller
    app = QApplication(sys.argv)
    controller = Controller()
    window = CurrentPatientGUI(controller)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()