# ### Task 4.6
# A singleton is a class that allows only a single instance of itself to be created
# and gives access to that created instance. Implement singleton logic inside your
# custom class using a method to initialize class instance.


class Sun:
    exist_instance = None

    def __new__(cls):
        if not Sun.exist_instance:
            cls.exist_instance = object.__new__(Sun)
            return cls.exist_instance
        else:
            return cls.exist_instance

    @classmethod
    def inst(cls):
        return cls()


p = Sun.inst()
f = Sun.inst()

s = Sun()
t = Sun()

print(p is f, (p, f))
print(s is t, (s, t))
