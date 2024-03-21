i = int(input("Berapa : "))

for x in range(1, i + 1):
    if (x % 3 == 0 and x % 4 == 0):
        print("OKYES")
    elif (x % 3 == 0):
        print("OK")
    elif (x % 4 == 0):
        print("YES")
    else :
        print(x)
