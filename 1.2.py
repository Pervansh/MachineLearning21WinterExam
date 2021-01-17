from random import random

# z = f(x, y)

eps = 1e-5
c = 1e-6
startValue = 5

def dzdx(x, y):
    return 36 * (x ** 5) + 8 * (y ** 2) * (x ** 3) + 20 * x + 6 * y - 6

def dzdy(x, y):
    return 4 * (x ** 4) * y + 6 * x + 20 * y

def z(x, y):
    return 6 * (x ** 6) + 2 * (x ** 4) + (y ** 2) + 10 * (x ** 2) + 6 * x * y + 10 * (y ** 2) - 6 * x + 4

v = complex(startValue * random(), startValue * random())
lastV = v + complex(2 * c, 2 * c)

while (abs(v - lastV) > c):
    lastV = v
    x = v.real
    y = v.imag
    v += -eps * complex(dzdx(x, y), dzdy(x, y))
    print(v - lastV)

print(v.real, ' ', v.imag)
print(z(v.real, v.imag))
