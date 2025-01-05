import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QVBoxLayout, QStackedWidget

from clinic.controller import Controller
from clinic.gui.create_patient_gui import CreatePatientGUI
from clinic.gui.search_patient_gui import SearchPatientGUI
from clinic.gui.retrieve_patients_gui import RetrievePatientGUI
from clinic.gui.update_patient_gui import UpdatePatientGUI
from clinic.gui.delete_patient_gui import DeletePatientGUI
from clinic.gui.list_patients_gui import ListPatientsGUI
from clinic.gui.current_patient_gui import CurrentPatientGUI
from clinic.gui.create_note_gui import CreateNoteGUI
from clinic.gui.retrieve_notes_gui import RetrieveNotesGUI
from clinic.gui.update_note_gui import UpdateNoteGUI
from clinic.gui.delete_note_gui import DeleteNoteGUI
from clinic.gui.list_patient_record_gui import ListPatientRecordGUI

from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException

class ClinicGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clinic System")
        self.controller = Controller()

        # stacked widget to switch between login and clinic
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.login_widget = self.create_login_widget()
        self.clinic_widget = self.create_clinic_widget()

        # widgets added to stacked layout
        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.clinic_widget)  
    
    def create_login_widget(self):
        """
        Purpose: Create the login screen.
        Return: login widget
        """
        self.setFixedSize(225, 250)
        widget = QWidget()
        layout = QVBoxLayout()

        label_username = QLabel("Username")
        self.text_username = QLineEdit()
        self.text_username.setFixedSize(200, 30)

        label_password = QLabel("Password")
        self.text_password = QLineEdit()
        self.text_password.setFixedSize(200, 30)
        
        # obscures password for privacy of user
        self.text_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.button_login = QPushButton("Login")
        self.button_login.setFixedSize(150, 40)
        self.button_quit = QPushButton("Quit")
        self.button_quit.setFixedSize(150, 40)

        layout.addWidget(label_username)
        layout.addWidget(self.text_username)
        layout.addWidget(label_password)
        layout.addWidget(self.text_password)
        layout.addWidget(self.button_login)
        layout.addWidget(self.button_quit)

        # connect login button to a method that switches to clinic once clicked
        # quit button connects to a method that stops the program
        self.button_login.clicked.connect(self.handle_login)
        self.button_quit.clicked.connect(self.quit_button_clicked)

        widget.setLayout(layout)
        return widget

    def create_clinic_widget(self):
        """
        Purpose: Create the clinic screen.
        Return: clinic widget
        """
        widget = QWidget()
        layout = QVBoxLayout()
        
        # all user story labels created
        label_welcome = QLabel("Welcome to the Clinic Main Menu")
        self.search_patient = QPushButton("Search patient by PHN")
        self.new_patient = QPushButton("Create new patient")
        self.retrieve_patient = QPushButton("Retrieve patients by name")
        self.update_patient = QPushButton("Update patient data")
        self.remove_patient = QPushButton("Delete patient")
        self.list_patients= QPushButton("List all patients")
        self.set_patient = QPushButton("Set current patient")
        self.create_note = QPushButton("Create new note")
        self.retrieve_notes = QPushButton("Retrieve notes")
        self.update_note= QPushButton("Update note")
        self.delete_note = QPushButton("Delete a note")
        self.list_notes = QPushButton("List full patient record")
        self.logout_button = QPushButton("Logout")
        
        # add the labels as widgets to window
        layout.addWidget(label_welcome)
        layout.addWidget(self.search_patient)
        layout.addWidget(self.new_patient)
        layout.addWidget(self.retrieve_patient)
        layout.addWidget(self.update_patient)
        layout.addWidget(self.remove_patient)
        layout.addWidget(self.list_patients)
        layout.addWidget(self.set_patient)
        layout.addWidget(self.create_note)
        layout.addWidget(self.retrieve_notes)
        layout.addWidget(self.update_note)
        layout.addWidget(self.delete_note)
        layout.addWidget(self.list_notes)
        layout.addWidget(self.logout_button)

        # connect each button to their respective GUI to open when clicked
        self.logout_button.clicked.connect(self.handle_logout)
        self.search_patient.clicked.connect(self.open_search_patient)
        self.new_patient.clicked.connect(self.open_create_patient)
        self.retrieve_patient.clicked.connect(self.open_retrieve_patient)
        self.update_patient.clicked.connect(self.open_update_patient)
        self.remove_patient.clicked.connect(self.open_delete_patient)
        self.list_patients.clicked.connect(self.open_list_patients)
        self.set_patient.clicked.connect(self.open_current_patient)
        self.create_note.clicked.connect(self.open_create_note)
        self.retrieve_notes.clicked.connect(self.open_retrieve_notes)
        self.update_note.clicked.connect(self.open_update_note)
        self.delete_note.clicked.connect(self.open_delete_note)
        self.list_notes.clicked.connect(self.open_list_notes)

        widget.setLayout(layout)
        return widget

    def handle_login(self):
        """
        Purpose: Handle login logic, send a welcome message if succesful and switch to clinic. 
                 Raise exceptions otherwise.
        """
        username = self.text_username.text()
        password = self.text_password.text()

        try:
            if self.controller.login(username, password):
                QMessageBox.information(self, "Login Successful", "Welcome, " + username + "!")  
                self.switch_to_clinic()  
        except DuplicateLoginException:
            QMessageBox.warning(self, "Login Failed", "User already is logged in.")
        except InvalidLoginException:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

        # clear the text from the text widgets after succeseful login
        self.text_username.setText("")
        self.text_password.setText("")

    def handle_logout(self):
        """
        Purpose: Handle logout logic. Switch back to window size for login, 
                and switch to login screen.
        """
        self.controller.logout()
        QMessageBox.information(self, "Logout", "You have been logged out.")
        self.setFixedSize(225, 250)
        self.stacked_widget.setCurrentIndex(0)  # Switch back to the login screen

    def switch_to_clinic(self):
        """
        Purpose : Switch to the clinic screen.
        """
        self.setFixedSize(500, 400)
        self.stacked_widget.setCurrentIndex(1)  # Switch to the clinic screen

    def open_search_patient(self):
        """
        Purpose: Open the search patient GUI.
        """
        self.search_patient_gui = SearchPatientGUI(self.controller)
        self.search_patient_gui.show()

    def open_create_patient(self):
        """
        Purpose: Open the create patient GUI.
        """
        self.add_patient_gui = CreatePatientGUI(self.controller)
        self.add_patient_gui.show()

    def open_retrieve_patient(self):
        """
        Purpose: Open the retrieve patients GUI.
        """
        self.retrieve_patient_gui = RetrievePatientGUI(self.controller)
        self.retrieve_patient_gui.show()

    def open_update_patient(self):
        """
        Purpose: Open the update patients GUI.
        """
        self.update_patient_gui = UpdatePatientGUI(self.controller)
        self.update_patient_gui.show()

    def open_delete_patient(self):
        """
        Purpose: Open the delete patients GUI.
        """
        self.remove_patient_gui = DeletePatientGUI(self.controller)
        self.remove_patient_gui.show()

    def open_list_patients(self):
        """
        Purpose: Open the list patients GUI.
        """
        self.list_patients_gui = ListPatientsGUI(self.controller)
        self.list_patients_gui.show()

    def open_current_patient(self):
        """
        Purpose: Open the current patient GUI.
        """
        self.current_patient_gui = CurrentPatientGUI(self.controller)
        self.current_patient_gui.show()

    def open_create_note(self):
        """
        Purpose: Open the create note GUI.
        """
        self.create_note_gui = CreateNoteGUI(self.controller)
        self.create_note_gui.show()

    def open_retrieve_notes(self):
        """
        Purpose: Open the retrieve notes GUI.
        """
        self.retrieve_notes_gui = RetrieveNotesGUI(self.controller)
        self.retrieve_notes_gui.show()

    def open_update_note(self):
        """
        Purpose: Open the update note GUI.
        """
        self.update_note_gui = UpdateNoteGUI(self.controller)
        self.update_note_gui.show()

    def open_delete_note(self):
        """
        Purpose: Open the delete note GUI.
        """
        self.delete_note_gui = DeleteNoteGUI(self.controller)
        self.delete_note_gui.show()

    def open_list_notes(self):
        """
        Purpose: Open the list notes GUI.
        """
        self.list_notes_gui = ListPatientRecordGUI(self.controller)
        self.list_notes_gui.show()

    def quit_button_clicked(self):
        """
        Purpose: Quit the program.
        """
        sys.exit()

def main():
    app = QApplication(sys.argv)
    window = ClinicGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
