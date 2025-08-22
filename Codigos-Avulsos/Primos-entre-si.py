a = int(input("Digite o valor de A: "))
b = int(input("Digite o valor de B: "))
if b > a:
    menor = a
else:
    menor = b
condicao = True
for i in range(2,menor+1):
    if a % i == 0 and b % i == 0:
        condicao = False
        break
    else:
        continue
if condicao:
    print("São primos entre si")
else:
    print("Não são primos entre si")