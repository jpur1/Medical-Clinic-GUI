from clinic.controller import Controller
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.cli.main_menu_cli import MainMenuCLI
from getpass import getpass

class ClinicCLI():

	def __init__(self):
		self.controller = Controller(autosave=True)
		self.main_menu_cli = MainMenuCLI(self.controller)
		self.login_menu()

	def login_menu(self):
		while True:
			self.print_login_menu()
			try:
				response = int(input('\nChoose your option: '))
			except ValueError:
				print('Please enter an integer number.')
				input('Type ENTER to continue.')
				continue
			if response == 1:
				if self.login():
					self.main_menu_cli.main_menu()
			elif response == 2:
				print('\nSESSION FINISHED.')
				break
			else:
				print('\nWRONG CHOICE. Please pick a choice between 1 and 2.')
				input('Type ENTER to continue.')
		return

	def print_login_menu(self):
		print('\n\nMEDICAL CLINIC SYSTEM\n\n')
		print('1 - Log in')
		print('2 - Quit')

	def login(self):
		try:
			print('LOGIN:')
			username = input('Username: ')
			password = getpass('Password: ')
			self.controller.login(username, password)
		except InvalidLoginException:
			print('\nLOGIN INCORRECT.')
			return False
		return True

if __name__ == '__main__':
	main()