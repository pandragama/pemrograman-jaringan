def cek_prima(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    print(n)

i = int(input("Sampe mana: "))
for x in range (1, i + 1):
    cek_prima(x)