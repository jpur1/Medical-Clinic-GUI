import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QTableView
from PyQt6.QtGui import QStandardItemModel, QStandardItem

from clinic.exception.illegal_access_exception import IllegalAccessException

class RetrievePatientGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Retrieve Existing Patients")
        self.setGeometry(100, 100, 625, 600)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()

        # Labels created, connect search button to retrieve patients method below
        self.label_name = QLabel("Enter Name:")
        self.text_name = QLineEdit()
        self.text_name.setPlaceholderText("Name of Patient")
        self.button_search = QPushButton("Search")
        self.button_search.clicked.connect(self.retrieve_patients)

        # Horizontal layout, add labels as widgets, then add overall to window
        text_layout = QHBoxLayout()
        text_layout.addWidget(self.label_name)
        text_layout.addWidget(self.text_name)
        text_layout.addWidget(self.button_search)
        layout.addLayout(text_layout)

        #  Create QTableView() & data model for column labels
        self.patient_table = QTableView()
        self.patient_model = QStandardItemModel()
        self.patient_model.setHorizontalHeaderLabels(
            ["PHN", "Name", "Birth Date", "Phone", "Email", "Address"])
        # Attach data model to the table
        self.patient_table.setModel(self.patient_model)
        layout.addWidget(self.patient_table)

        main_widget.setLayout(layout)

    def retrieve_patients(self):
        """
        Purpose: Store search input, if none tell user to search some text. Retrieve patients, then
                 pass that to populate table. Otherwise, raise excpetions.
        """
        search_string = self.text_name.text().strip()
        if not search_string:
            QMessageBox.warning(self, "Input Error", "Please enter a name to search.")
            return
        
        try:
            patients = self.controller.retrieve_patients(search_string)
            self.populate_table(patients)
        except ValueError:
            QMessageBox.warning(self, "Value Error", "Invalid input, try again.")
        except IllegalAccessException:
            QMessageBox.warning(self, "Access Error", "Cannot retrieve when user is not logged in.")

    def populate_table(self, patients):
        """
        Purpose: Clear the existing rows for a fresh start, then move through patients list,
                 making each row a new patient and storing each attribute to it's attribute
                 column.
        """
        self.patient_model.setRowCount(0)  # Clear existing rows

        # Iterate through patients to add to model
        for patient in patients:
            # New row for each patient, then append each attribute to respective column
            self.patient_model.appendRow([
                QStandardItem(str(patient.phn)),
                QStandardItem(patient.name),
                QStandardItem(patient.birth_date),
                QStandardItem(patient.phone),
                QStandardItem(patient.email),
                QStandardItem(patient.address),
            ])

def main():
    from clinic.controller import Controller
    app = QApplication(sys.argv)
    controller = Controller()
    window = RetrievePatientGUI(controller)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
