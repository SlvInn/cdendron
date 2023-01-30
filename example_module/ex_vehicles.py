
class Vehicle:
    """ Ex. of parent class """
    
    # class attribute
    brand_name = 'Renault'
    

    def __init__(self, version,price,color):
        
        # instance attributes
        self.price   = price
        self.version = version
        self.color   = color

    
    def from_price(self, cls, name, price): # this won't generate  warning in the creating the graph, since self found in input
        # ind_price = dollar * 76
        # create new Vehicle object
        return cls(name, (price * 75))

    def show(self):
        print(self.name, self.price)

class Car(Vehicle):
    """ Ex. of child class """
    
    model_name = 'Clio'
    
    def __init__(self, version,price,color,owner_name):
        super().__init__(version,price,color)
        self.owner = owner_name
    
    def average(self, distance, fuel_used):
        mileage = distance / fuel_used
        print(self.name, 'Mileage', mileage)


# define a complitely separated class
# # renault_us = Car('Storia', 25000,'red')
# # renault_us.show()

# # # class method of parent class is available to child class
# # # this will return the object of calling class
# # renault_ind = Car.from_price('sport', 35000,'blue')
# # renault_ind.show()

# # # check type
# # print(type(renault_ind))