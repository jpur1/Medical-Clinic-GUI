from clinic.controller import Controller
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

class AppointmentMenuCLI():

    def __init__(self, controller):
        self.controller = controller

    def appointment_menu(self):
        while True:
            self.print_appointment_menu()
            try:
                response = int(input('\nChoose your option: '))
            except ValueError:
                print('Please enter an integer number.')
                input('Type ENTER to continue.')
                continue
            if response == 1:
                self.create_note()
                input('Type ENTER to continue.')
            elif response == 2:
                self.retrieve_notes()
                input('Type ENTER to continue.')
            elif response == 3:
                self.update_note()
                input('Type ENTER to continue.')
            elif response == 4:
                self.delete_note()
                input('Type ENTER to continue.')
            elif response == 5:
                self.list_full_patient_record()
                input('Type ENTER to continue.')
            elif response == 6:
                self.end_appointment()
                print('\nAPPOINTMENT FINISHED.')
                break
            else:
                print('\nWRONG CHOICE. Please pick a choice between 1 and 6.')
                input('Type ENTER to continue.')
        return

    def print_appointment_menu(self):
        print('\n\nMEDICAL CLINIC SYSTEM - APPOINTMENT MENU\n\n')
        print('1 - Add note to patient record')
        print('2 - Retrieve notes from patient record by text')
        print('3 - Change note from patient record')
        print('4 - Remove note from patient record')
        print('5 - List full patient record')
        print('6 - Finish appointment')

    def create_note(self):
        print('ADD NOTE TO PATIENT RECORD:')
        try:
            text = input()
            self.controller.create_note(text)
            print('\nNOTE ADDED TO THE SYSTEM.')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except NoCurrentPatientException:
            print('\nERROR ADDING NEW NOTE.') 
            print('Cannot add a note without a valid current patient.')

    def retrieve_notes(self):
        print('RETRIEVE NOTES FROM PATIENT RECORD BY TEXT:')
        try:
            search_string = input('Search for: ')
            found_notes = self.controller.retrieve_notes(search_string)
            if found_notes:
                print('\nNotes found for %s:\n' % search_string)
                for note in found_notes:
                    self.print_note_data(note)
            else:
                print('\nNo notes found for: %s\n' % search_string)
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except NoCurrentPatientException:
            print('\nERROR ADDING NEW NOTE.') 
            print('Cannot add a note without a valid current patient.')

    # helper method to print note data
    def print_note_data(self, note):
        print('Note #%d, from %s' % (note.code, note.timestamp))
        print('%s\n' % note.text)

    def update_note(self):
        print('CHANGE NOTE FROM PATIENT RECORD:')
        try:
            code = int(input('Note number: '))
            note = self.controller.search_note(code)
            if note:
                self.print_note_data(note)
                confirm = input('Are you sure you want to change note #%s (y/n)? ' % note.code)
                if confirm.lower() == 'y':
                    print('Type new text for note:')
                    new_text = input()
                    self.controller.update_note(code, new_text)
            else:
                print('\nERROR CHANGING NOTE FROM PATIENT RECORD.')
                print('There is no note registered with this number.')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except NoCurrentPatientException:
            print('\nERROR REMOVING NOTE.') 
            print('Cannot remove a note without a valid current patient.')

    def delete_note(self):
        print('REMOVE NOTE FROM PATIENT RECORD:')
        try:
            code = int(input('Note number: '))
            note = self.controller.search_note(code)
            if note:
                self.print_note_data(note)
                confirm = input('Are you sure you want to remove note #%s (y/n)? ' % note.code)
                if confirm.lower() == 'y':
                    self.controller.delete_note(code)
            else:
                print('\nERROR REMOVING NOTE FROM RECORD.')
                print('There is no note registered with this number.')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except NoCurrentPatientException:
            print('\nERROR REMOVING NOTE.') 
            print('Cannot remove a note without a valid current patient.')

    def list_full_patient_record(self):
        print('LIST FULL PATIENT RECORD:\n')
        try:
            notes = self.controller.list_notes()
            if notes:
                for note in notes:
                    self.print_note_data(note)
            else:
                print('\nPatient record is empty.\n')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except NoCurrentPatientException:
            print('\nERROR LISTING PATIENT RECORD.') 
            print('Cannot list the record without a valid current patient.')

    # helper method to print note data
    def print_note_data(self, note):
        print('Note #%d, from %s' % (note.code, note.timestamp))
        print('%s\n' % note.text)

    def end_appointment(self):
        try:
            self.controller.unset_current_patient()
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
