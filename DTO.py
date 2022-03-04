class Hat:
    def __init__(self, hat_id, topping, supplier, quantity):
        self.id = hat_id
        self.topping = topping
        self.supplier = supplier
        self.quantity = quantity


class Supplier:
    def __init__(self, sup_id, name):
        self.id = sup_id
        self.name = name


class Order:
    def __init__(self, order_id, location, hat):
        self.id = order_id
        self.location = location
        self.hat = hat
