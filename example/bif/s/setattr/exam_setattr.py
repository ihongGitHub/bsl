# The setattr() method sets the value of given attribute of an object.

class Person:
    name = 'Adam'

p = Person()
print('Before modification:', p.name)

# setting name to 'John'
setattr(p, 'name', 'John')

print('After modification:', p.name)
