# ### Task 4.4
# Create hierarchy out of birds.
# Implement 4 classes:
# * class `Bird` with an attribute `name` and methods `fly` and `walk`.
# * class `FlyingBird` with attributes `name`, `ration`, and with the same methods. `ration` must have default value.
# Implement the method `eat` which will describe its typical ration.
# * class `NonFlyingBird` with same characteristics but which obviously without attribute `fly`.
# Add same "eat" method but with other implementation regarding the swimming bird tastes.
# * class `SuperBird` which can do all of it: walk, fly, swim and eat.
# But be careful which "eat" method you inherit.
#
# Implement str() function call for each class.


class Bird:
    def __init__(self, name):
        self.name = name

    def fly(self):
        print(f"{self.name} undecided about flying")

    def walk(self):
        print(f"{self.name} bird can walk")


class FlyingBird(Bird):
    def __init__(self, name, ration='grains'):
        super().__init__(name)
        self.ration = ration

    def fly(self):
        print(f"{self.name} bird can fly")

    def eat(self):
        print(f"{self.name} eats mostly {self.ration}")

    def __str__(self):
        return f"{self.name} can walk and fly"


class NonFlyingBird(Bird):
    def __init__(self, name, ration):
        super().__init__(name)
        self.ration = ration

    def __getattribute__(self, item):
        if item == "fly":
            raise AttributeError(f"'{self.name}' object has no attribute 'fly'")
        else:
            return object.__getattribute__(self, item)

    def eat(self):
        print(f'{self.name} eats mostly {self.ration}')

    def swim(self):
        print(f'{self.name} bird can swim')

    def __str__(self):
        return f"{self.name} can walk and swim"


class SuperBird(FlyingBird, NonFlyingBird):
    def __init__(self, name, ration='fish'):
        super(FlyingBird, self).__init__(name, ration)

    def __getattribute__(self, item):
        return object.__getattribute__(self, item)

    def __str__(self):
        return f"{self.name} can walk, swim and fly"


b = Bird('Any')
b.walk()
print("-" * 50)

fb = FlyingBird("Pigeon")
fb.eat()
fb.fly()
fb.walk()
print(fb)
print("-" * 50)

nb = NonFlyingBird('Penguin', ration='fish')
nb.eat()
nb.swim()
nb.walk()
nb.fly()
print(nb)
print("-" * 50)

sb = SuperBird('Gull')
sb.eat()
sb.swim()
sb.walk()
sb.fly()
print(sb)
print(SuperBird.__mro__)
