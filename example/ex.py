# Solve the quadratic equation ax**2 + bx + c = 0


class myclass:


    pass
    pass

    x = 0

# import complex math module
import cmath # test
from tqdm import tqdm
a = 1
b = 5
c = 6

# calculate the discriminant
d = (b**2) - (4*a*c)

# find two solutions
sol1 = (-b-cmath.sqrt(d))/(2*a)
sol2 = (-b+cmath.sqrt(d))/(2*a)


print('The solution are {0}, {1}, and {2}'.format(sol1,sol2))