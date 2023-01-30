# Exemple classes from 
# https://pynative.com/python-class-method/



from datetime import date

class Student:
    
    # class attribute
    school_name = 'B. Peruzzi'
    
    def __init__(self, name, age):
        
        # instance attributes
        self.name = name
        self.age = age

    @classmethod
    def calculate_age(cls, name, birth_year): # this will generate  warning in the creating the graph, since no self found in input (no signature)
        # calculate age an set it as a age
        # return new object
        return cls(name, date.today().year - birth_year)

    def show(self):
        print(self.name + "'s age is: " + str(self.age))


# # # E.g., call the class with: 
# # # jessa = Student('Jessa', 20)
# # # jessa.show()

# # # # create new object using the factory method
# # # joy = Student.calculate_age("Joy", 1995)
# # # joy.show()
