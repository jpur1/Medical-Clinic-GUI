import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from controller import Controller, IllegalOperationException

class ProductGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = Controller()
        self.setWindowTitle("Products")

        layout1 = QGridLayout()

        label_code = QLabel("Product Code")
        self.text_code = QLineEdit()
        self.text_code.setInputMask('00000000')
        label_description = QLabel("Description")
        self.text_description = QLineEdit()
        label_price = QLabel("Price")
        self.text_price = QLineEdit()

        layout1.addWidget(label_code, 0, 0)
        layout1.addWidget(self.text_code, 0, 1)
        layout1.addWidget(label_description, 1, 0)
        layout1.addWidget(self.text_description, 1, 1)
        layout1.addWidget(label_price, 2, 0)
        layout1.addWidget(self.text_price, 2, 1)

        layout2 = QHBoxLayout()

        self.button_clear = QPushButton("Clear")
        label_search_code = QLabel("Code:")
        self.text_search_code = QLineEdit()
        self.text_search_code.setInputMask('00000000')
        self.button_search = QPushButton("Search")
        self.button_create = QPushButton("Create")
        self.button_search.setEnabled(False)
        self.button_create.setEnabled(False)
        layout2.addWidget(self.button_clear)
        layout2.addWidget(label_search_code)
        layout2.addWidget(self.text_search_code)
        layout2.addWidget(self.button_search)
        layout2.addWidget(self.button_create)

        layout3 = QVBoxLayout()

        top_widget = QWidget()
        top_widget.setLayout(layout1)
        bottom_widget = QWidget()
        bottom_widget.setLayout(layout2)
        layout3.addWidget(top_widget)
        layout3.addWidget(bottom_widget)
        widget = QWidget()
        widget.setLayout(layout3)

        self.setCentralWidget(widget)

        # define widgets' initial state
        self.text_code.setEnabled(True)
        self.text_description.setEnabled(True)
        self.text_price.setEnabled(True)
        self.button_clear.setEnabled(True)
        self.button_search.setEnabled(False)
        self.button_create.setEnabled(False)

        # handle text change to enable/disable buttons
        self.text_code.textChanged.connect(self.product_text_changed)
        self.text_description.textChanged.connect(self.product_text_changed)
        self.text_price.textChanged.connect(self.product_text_changed)
        self.text_search_code.textChanged.connect(self.search_code_text_changed)

        # connect the buttons' clicked signals to the slots below
        self.button_clear.clicked.connect(self.clear_button_clicked)
        self.button_search.clicked.connect(self.search_button_clicked)
        self.button_create.clicked.connect(self.create_button_clicked)

    def product_text_changed(self):
        if self.text_code.text() and self.text_description.text() and self.text_price.text():
            self.button_create.setEnabled(True)
        else:
            self.button_create.setEnabled(False)

    def search_code_text_changed(self):
        if self.text_search_code.text():
            self.button_search.setEnabled(True)
        else:
            self.button_search.setEnabled(False)

    def clear_button_clicked(self):
        ''' clear the fields '''
        self.text_code.clear()
        self.text_description.clear()
        self.text_price.clear()
        self.text_search_code.clear()
        self.text_code.setEnabled(True)
        self.text_description.setEnabled(True)
        self.text_price.setEnabled(True)
        self.button_search.setEnabled(False)

    def search_button_clicked(self):
        ''' search product '''
        # TODO: First, get the key from the search text. Then call controller.search_product()
        

        # after storing the returned product in a variable, check this variable
        # TODO: if you found a product with that code, show it in the QLineEdits
        # and do not allow the texts to be edited
        # also, do not allow more searches (let the Clear button allow searches back again)
        
        try:
            key = int(self.text_search_code.text())
            product = self.controller.search_product(key)

            if product:
                #product details
                self.text_code.setText("%d" % product.code)
                self.text_description.setText(product.description)
                self.text_price.setText("%.2f" % product.price)

                #disable fields
                self.text_code.setEnabled(False)
                self.text_description.setEnabled(False)
                self.text_price.setEnabled(False)

                #disable the search until clear button
                self.button_search.setEnabled(False)
            else:
                QMessageBox.warning(self, "Product Not Found", f"No product found with code: {key}")
                self.clear_button_clicked()
        
        except IllegalOperationException as e:
            QMessageBox.critical(self, "Error", str(e))



    def create_button_clicked(self):
        ''' add new product '''
        # TODO: Use a try-except block to create a product.
        # Inside the try block, get the strings from the QLineEdits, do your conversions
        # and call controller.create_product().
        # After successful creation show a message box. Then, clear the fields.
        try:
            code = int(self.text_code.text())
            description = str(self.text_description.text())
            price = float(self.text_price.text())

            self.controller.create_product(code, description, price)

            # success
        
            QMessageBox.information(self, "Success", f"Product {code} created successfully!")
            self.clear_button_clicked()

            self.text_code.setText("")
            self.text_description.setText("")
            self.text_price.setText("")

        except(IllegalOperationException):
        # TODO: In the except block, show an intelligible warning that one can only add
        # new products if the code is not registered in the system. 
            QMessageBox.warning(self, "Cannot Create", "Code is already registered. Try again.")

app = QApplication(sys.argv)
window = ProductGUI()
window.show()
app.exec()
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from controller import Controller, IllegalOperationException

class ProductGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = Controller()
        self.setWindowTitle("Products")

        layout1 = QGridLayout()

        label_code = QLabel("Product Code")
        self.text_code = QLineEdit()
        self.text_code.setInputMask('00000000')
        label_description = QLabel("Description")
        self.text_description = QLineEdit()
        label_price = QLabel("Price")
        self.text_price = QLineEdit()

        layout1.addWidget(label_code, 0, 0)
        layout1.addWidget(self.text_code, 0, 1)
        layout1.addWidget(label_description, 1, 0)
        layout1.addWidget(self.text_description, 1, 1)
        layout1.addWidget(label_price, 2, 0)
        layout1.addWidget(self.text_price, 2, 1)

        layout2 = QHBoxLayout()

        self.button_clear = QPushButton("Clear")
        label_search_code = QLabel("Code:")
        self.text_search_code = QLineEdit()
        self.text_search_code.setInputMask('00000000')
        self.button_search = QPushButton("Search")
        self.button_create = QPushButton("Create")
        self.button_search.setEnabled(False)
        self.button_create.setEnabled(False)
        layout2.addWidget(self.button_clear)
        layout2.addWidget(label_search_code)
        layout2.addWidget(self.text_search_code)
        layout2.addWidget(self.button_search)
        layout2.addWidget(self.button_create)

        layout3 = QVBoxLayout()

        top_widget = QWidget()
        top_widget.setLayout(layout1)
        bottom_widget = QWidget()
        bottom_widget.setLayout(layout2)
        layout3.addWidget(top_widget)
        layout3.addWidget(bottom_widget)
        widget = QWidget()
        widget.setLayout(layout3)

        self.setCentralWidget(widget)

        # define widgets' initial state
        self.text_code.setEnabled(True)
        self.text_description.setEnabled(True)
        self.text_price.setEnabled(True)
        self.button_clear.setEnabled(True)
        self.button_search.setEnabled(False)
        self.button_create.setEnabled(False)

        # handle text change to enable/disable buttons
        self.text_code.textChanged.connect(self.product_text_changed)
        self.text_description.textChanged.connect(self.product_text_changed)
        self.text_price.textChanged.connect(self.product_text_changed)
        self.text_search_code.textChanged.connect(self.search_code_text_changed)

        # connect the buttons' clicked signals to the slots below
        self.button_clear.clicked.connect(self.clear_button_clicked)
        self.button_search.clicked.connect(self.search_button_clicked)
        self.button_create.clicked.connect(self.create_button_clicked)

    def product_text_changed(self):
        if self.text_code.text() and self.text_description.text() and self.text_price.text():
            self.button_create.setEnabled(True)
        else:
            self.button_create.setEnabled(False)

    def search_code_text_changed(self):
        if self.text_search_code.text():
            self.button_search.setEnabled(True)
        else:
            self.button_search.setEnabled(False)

    def clear_button_clicked(self):
        ''' clear the fields '''
        self.text_code.clear()
        self.text_description.clear()
        self.text_price.clear()
        self.text_search_code.clear()
        self.text_code.setEnabled(True)
        self.text_description.setEnabled(True)
        self.text_price.setEnabled(True)
        self.button_search.setEnabled(False)

    def search_button_clicked(self):
        ''' search product '''
        # TODO: First, get the key from the search text. Then call controller.search_product()
        

        # after storing the returned product in a variable, check this variable
        # TODO: if you found a product with that code, show it in the QLineEdits
        # and do not allow the texts to be edited
        # also, do not allow more searches (let the Clear button allow searches back again)
        
        try:
            key = int(self.text_search_code.text())
            product = self.controller.search_product(key)

            if product:
                #product details
                self.text_code.setText("%d" % product.code)
                self.text_description.setText(product.description)
                self.text_price.setText("%.2f" % product.price)

                #disable fields
                self.text_code.setEnabled(False)
                self.text_description.setEnabled(False)
                self.text_price.setEnabled(False)

                #disable the search until clear button
                self.button_search.setEnabled(False)
            else:
                QMessageBox.warning(self, "Product Not Found", f"No product found with code: {key}")
                self.clear_button_clicked()
        
        except IllegalOperationException as e:
            QMessageBox.critical(self, "Error", str(e))



    def create_button_clicked(self):
        ''' add new product '''
        # TODO: Use a try-except block to create a product.
        # Inside the try block, get the strings from the QLineEdits, do your conversions
        # and call controller.create_product().
        # After successful creation show a message box. Then, clear the fields.
        try:
            code = int(self.text_code.text())
            description = str(self.text_description.text())
            price = float(self.text_price.text())

            self.controller.create_product(code, description, price)

            # success
        
            QMessageBox.information(self, "Success", f"Product {code} created successfully!")
            self.clear_button_clicked()

            self.text_code.setText("")
            self.text_description.setText("")
            self.text_price.setText("")

        except(IllegalOperationException):
        # TODO: In the except block, show an intelligible warning that one can only add
        # new products if the code is not registered in the system. 
            QMessageBox.warning(self, "Cannot Create", "Code is already registered. Try again.")

app = QApplication(sys.argv)
window = ProductGUI()
window.show()
app.exec()
