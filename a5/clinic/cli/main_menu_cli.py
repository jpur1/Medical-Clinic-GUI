from clinic.controller import Controller
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.cli.appointment_menu_cli import AppointmentMenuCLI

class MainMenuCLI():

    def __init__(self, controller):
        self.controller = controller
        self.appointment_menu_cli = AppointmentMenuCLI(self.controller)


    def main_menu(self):
        while True:
            self.print_main_menu()
            try:
                response = int(input('\nChoose your option: '))
            except ValueError:
                print('Please enter an integer number.')
                input('Type ENTER to continue.')
                continue
            if response == 1:
                self.create_patient()
                input('Type ENTER to continue.')
            elif response == 2:
                self.search_patient()
                input('Type ENTER to continue.')
            elif response == 3:
                self.retrieve_patients_by_name()
                input('Type ENTER to continue.')
            elif response == 4:
                self.update_patient()
                input('Type ENTER to continue.')
            elif response == 5:
                self.delete_patient()
                input('Type ENTER to continue.')
            elif response == 6:
                self.list_all_patients()
                input('Type ENTER to continue.')
            elif response == 7:
                self.start_appointment()
                input('Type ENTER to continue.')
            elif response == 8:
                if self.logout():
                    print('\nLOGGED OUT.')
                    input('Type ENTER to continue.')
                    break
            else:
                print('\nWRONG CHOICE. Please pick a choice between 1 and 8.')
                input('Type ENTER to continue.')
        return

    def print_main_menu(self):
        print('\n\nMEDICAL CLINIC SYSTEM - MAIN MENU\n\n')
        print('1 - Add new patient')
        print('2 - Search patient by PHN')
        print('3 - Retrieve patients by name')
        print('4 - Change patient data')
        print('5 - Remove patient')
        print('6 - List all patients')
        print('7 - Start appointment with patient')
        print('8 - Log out')

    def create_patient(self):
        print('ADD NEW PATIENT:')
        try:
            phn = int(input('Personal Health Number (PHN): '))
            name = input('Full name: ')
            birth_date = input('Birth date (YYYY-MM-DD): ')
            phone = input('Phone number: ')
            email = input('Email: ')
            address = input('Address: ')
            self.controller.create_patient(phn, name, birth_date, phone, email, address)
            print('\nPATIENT ADDED TO THE SYSTEM.')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except IllegalOperationException:
            print('\nERROR ADDING NEW PATIENT.') 
            print('There is a patient already registered with PHN %d.' % phn)

    def search_patient(self):
        print('SEARCH PATIENT:')
        try:
            phn = int(input('Personal Health Number (PHN): '))
            patient = self.controller.search_patient(phn)
            if patient:
                self.print_patient_data(patient)
            else:
                print('\nThere is no patient registered with this PHN.')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')

    # helper method to print patient data
    def print_patient_data(self, patient):
        print('\nPATIENT:')
        print('PHN: %d' % patient.phn)
        print('Name: %s' % patient.name)
        print('Birth date: %s' % patient.birth_date)
        print('Phone: %s' % patient.phone)
        print('Email: %s' % patient.email)
        print('Address: %s\n' % patient.address)

    def retrieve_patients_by_name(self):
        print('RETRIEVE PATIENTS BY NAME:')
        try:
            search_string = input('Search for: ')
            found_patients = self.controller.retrieve_patients(search_string)
            if found_patients:
                print('\nPatients found with name %s:\n' % search_string)
                for patient in found_patients:
                    print(patient)
            else:
                print('\nNo patients found with name: %s\n' % search_string)
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')


    def update_patient(self):
        print('CHANGE PATIENT DATA:')
        try:
            original_phn = int(input('Personal Health Number (PHN): '))
            patient = self.controller.search_patient(original_phn)
            if patient:
                self.print_patient_data(patient)
                print('Type the new data value or enter for each field that should keep the old data: ')
                phn = input('Personal Health Number (PHN): ')
                name = input('Full name: ')
                birth_date = input('Birth date (YYYY-MM-DD): ')
                phone = input('Phone number: ')
                email = input('Email: ')
                address = input('Address: ')

                # update only fields that were not empty
                phn = int(phn) if phn !='' else patient.phn
                name = name if name !='' else patient.name
                birth_date = birth_date if birth_date !='' else patient.birth_date
                phone = phone if phone !='' else patient.phone
                email = email if email !='' else patient.email
                address = address if address !='' else patient.address

                confirm = input('\nAre you sure you want to change patient data %s (y/n)? ' % patient.name)
                if confirm.lower() == 'y':
                    self.controller.update_patient(original_phn, phn, name, birth_date, phone, email, address)
                    print('\nPATIENT DATA CHANGED.')
            else:
                print('\nERROR CHANGING PATIENT DATA.')
                print('There is no patient registered with this PHN.')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except IllegalOperationException:
            print('\nERROR CHANGING PATIENT DATA.')
            if self.controller.current_patient:
                if self.controller.current_patient.phn == phn:
                    print('Cannot change the current patient data. Finish appointment first.')
            else:
                print('Cannot change patient data to a new PHN that is already registered in the system.')


    def delete_patient(self):
        print('REMOVE PATIENT:')
        try:
            phn = int(input('Personal Health Number (PHN): '))
            patient = self.controller.search_patient(phn)
            if patient:
                self.print_patient_data(patient)
                confirm = input('\nAre you sure you want to remove patient %s (y/n)? ' % patient.name)
                if confirm.lower() == 'y':
                    self.controller.delete_patient(phn)
                    print('\nPATIENT REMOVED FROM THE SYSTEM.')
            else:
                print('\nERROR REMOVING PATIENT.')
                print('There is no patient registered with this PHN.')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except IllegalOperationException:
            print('\nERROR REMOVING PATIENT.')
            if self.controller.current_patient:
                if self.controller.current_patient.phn == phn:
                    print('Cannot remove the current patient. Finish appointment first.')
            else:
                print('Cannot remove a patient that is not registered in the system.')

    def list_all_patients(self):
        print('LIST ALL PATIENTS:\n')
        try:
            patients = self.controller.list_patients()
            if patients:
                for patient in patients:
                    print(patient)
            else:
                print('\nNo patients registered in the clinic.\n')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')

    def start_appointment(self):
        print('START APPOINTMENT:')
        try:
            phn = int(input('Personal Health Number (PHN): '))
            self.controller.set_current_patient(phn)
            current_patient = self.controller.get_current_patient()
            self.print_patient_data(current_patient)
            self.appointment_menu_cli.appointment_menu()
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except IllegalOperationException:
            print('\nERROR STARTING APPOINTMENT.') 
            print('There is no patient registered with PHN %d.' % phn)

    def logout(self):
        try:
            self.controller.logout()
        except InvalidLogoutException:
            print('\nUSER WAS ALREADY LOGGED OUT.')
            return False
        return True

