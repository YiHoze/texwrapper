from sys import argv 
from math import factorial

try:
    if len(argv) is 1:
        n = int(input("To get the factorial, enter a number: "))
    else:
        n = int(argv[1])
    r = factorial(n)
    r = format(r, ',')
    print(r)
except ValueError:
    print("That was no valid number.")