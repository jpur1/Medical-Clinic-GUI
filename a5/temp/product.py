class Product:
  def __init__(self, code, description, price):
    # code will be the key
    self.code = code
    self.description = description
    self.price = price

  def __str__(self):
    return "code: %d, description: %s, price: %.2f" % \
     (self.code, self.description, self.price)

  def __repr__(self):
    return "code: %r, description: %r, price: %r" % \
     (self.code, self.description, self.price)

  def __eq__(self, other):
    return self.code  == other.code and self.description == other.description \
     and self.price == other.price
