import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QVBoxLayout

from clinic.exception.illegal_access_exception import IllegalAccessException

class SearchPatientGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Search Patient")
        self.setGeometry(100, 100, 400, 200)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()

        # Create labels
        self.label_phn = QLabel("Enter PHN:")
        self.text_phn = QLineEdit()
        self.text_phn.setPlaceholderText("Personal Health Number")

        # Add labels as widget to window
        layout.addWidget(self.label_phn)
        layout.addWidget(self.text_phn)

        # Connect search button to search patient method
        self.button_search = QPushButton("Search")
        self.button_search.clicked.connect(self.search_patient)

        layout.addWidget(self.button_search)

        self.label_result = QLabel("")
        layout.addWidget(self.label_result)

        main_widget.setLayout(layout)


    def search_patient(self):
        """
        Purpose: Store phn that was inputted, search the patient in controller, then display
                 the patient found. Otherwise, raise exceptions.
        """
        try:
            phn = int(self.text_phn.text().strip())
            patient = self.controller.search_patient(phn)
            self.label_result.setText(f"Patient Found:\n{patient}")
        except ValueError:
            QMessageBox.warning(self, "Value Error", "Invalid input, try again.")
        except IllegalAccessException:
            QMessageBox.warning(self, "Access Error", "Cannot search when user is not logged in.")

def main():
    from clinic.controller import Controller
    app = QApplication(sys.argv)
    controller = Controller()
    window = SearchPatientGUI(controller)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
