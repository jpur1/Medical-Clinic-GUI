from json import JSONDecoder
from product import Product

class ProductDecoder(JSONDecoder):
  def __init__(self, *args, **kwargs):
    super().__init__(object_hook=self.object_hook, *args, **kwargs)

  def object_hook(self, dct):
    if '__type__' in dct and dct['__type__'] == 'Product':
      return Product(dct['code'], dct['description'], dct['price'])
    return dct
