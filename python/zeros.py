from sys import argv

if len(argv) is 1:
    number = input("It will be displayed \
how many zeros the multiplication \
1 up to a given number has at the tail. \
\nEnter a number: ")
else:
    number = argv[1]

try:
    number = int(number)
except ValueError:
    print("That was no valid number.")
    exit()

count = 0
i = 1
while True:
    factor = number / 5 ** i
    if factor > 1:
        count = count + factor
        i += 1
    else:
        break
count = int(count)
print(count)

# result = 1
# i = 1
# while i <= number:
#     result = result * i
#     # print(result)
#     i += 1
# result = str(result)
# print(result)

# i = len(result) - 1
# count = 0
# while True:
#     if result[i] == '0':
#         count += 1
#         i -= 1        
#     else:
#         break
# print(count)