import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QVBoxLayout, QTableView
from PyQt6.QtGui import QStandardItemModel, QStandardItem

from clinic.exception.illegal_access_exception import IllegalAccessException

class ListPatientsGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("List All Existing Patients")
        self.setGeometry(100, 100, 625, 600)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()

        # Create QTableView() & data model for column labels
        self.patient_table = QTableView()
        self.patient_model = QStandardItemModel()
        self.patient_model.setHorizontalHeaderLabels(
            ["PHN", "Name", "Birth Date", "Phone", "Email", "Address"])
        # Attach data model to the table
        self.patient_table.setModel(self.patient_model)
        layout.addWidget(self.patient_table)

        main_widget.setLayout(layout)
        self.list_patients()

    def list_patients(self):
        """
        Purpose: List all the patients, use those to send to populate table method. 
                 Otherwise, raise exceptions.
        """
        try:
            patients = self.controller.list_patients()
            self.populate_table(patients)
        except IllegalAccessException:
            QMessageBox.warning(self, "Access Error", "Cannot list when user is not logged in.")

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
    window = ListPatientsGUI(controller)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
