i = 1000
while i < 10000:
    digit = [int(j) for j in str(i)]
    if digit[3] != 0 and digit[0] != 0:
        val = digit[3] * (digit[0]**digit[3] + digit[0]/digit[3] - digit[3]/digit[0])
        if val == i:
            break
    i += 1
print(int(val))