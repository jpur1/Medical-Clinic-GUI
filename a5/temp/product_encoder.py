from json import JSONEncoder
from product import Product

class ProductEncoder(JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Product):
      return {"__type__": "Product", "code": obj.code, "description": obj.description, "price": obj.price}
    return super().default(obj)
