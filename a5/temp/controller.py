from product import Product
from product_decoder import ProductDecoder
from product_encoder import ProductEncoder
from json import loads, dumps

class Controller:
    def __init__(self):
        self.filename = 'products.json'
        try:
            self.products = self.load_products()
        except:
            self.products = []

    def load_products(self):
        products = []
        with open(self.filename, 'r') as file:
            for product_json in file:
                product = loads(product_json, cls=ProductDecoder)
                products.append(product)
        return products

    def save_products(self):
        with open(self.filename, 'w') as file:
            for product in self.products:
                product_json = dumps(product, cls=ProductEncoder)
                file.write("%s\n" % product_json)

    def search_product(self, key):
        for product in self.products:
            if (product.code == key):
                return product
        return None

    def create_product(self, code, description, price):
        if not self.search_product(code):
            product = Product(code, description, price)
            self.products.append(product)
            self.save_products()
        else:
            raise IllegalOperationException("Error adding product. There is already a product with code %d." % code)


class IllegalOperationException(Exception):
    ''' Illegal Operation '''