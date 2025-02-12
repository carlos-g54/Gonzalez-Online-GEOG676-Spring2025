#storing the value of pi as pie
pie = 3.14159

#create classes that define shape and measurements required for calculation
class shape():
    def __init__(self):
        pass

class Rectangle(shape):
    def __init__(self, l, w):
        self.length = l
        self.width = w
        
    def getArea(self):
        return self.length * self.width
        
class Circle(shape):
    def __init__(self, r):
        self.radius = r

    def getArea(self):
        return self.radius * pie * self.radius

class Triangle(shape):
    def __init__(self, b, h):
        self.base = b
        self.height = h

    def getArea(self):
        return self.base * 0.5 * self.height
    
#Open file as read only
file = open(r"C:\DevSource\Gonzalez-Online-GEOG676-Spring2025\Labs\Lab_03\shape.txt")
lines = file.readlines()
file.close()


#Read line by line. if the first index matches a shape name, it calculates the area. If it does not match, 
#it moves on to the next shape until the list is exhausted, then moves on to next line in the source list.
for line in lines:
    components = line.split(',')
    shape = components[0]

    if shape == 'Rectangle':
        rect = Rectangle(int(components[1]), int(components[2]))
        print('Area of the rectangle is',"{:.2f}".format(rect.getArea()))

    elif shape == 'Circle':
        circ = Circle(int(components[1]))
        print('Area of the circle is',"{:.2f}".format(circ.getArea()))

    elif shape == 'Triangle':
        trian = Triangle(int(components[1]), int(components[2]))
        print('Area of the triangle is',"{:.2f}".format(trian.getArea()))

    else:
        pass


