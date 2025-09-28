import time
import random

def calcular_operacoes():
    print("Iniciando processamento...")
    
    numeros = [random.randint(1, 100) for _ in range(10)]
    print(f"Números gerados: {numeros}")
    
    soma = sum(numeros)
    media = soma / len(numeros)
    maior = max(numeros)
    menor = min(numeros)
    
    print(f"Soma: {soma}")
    print(f"Media: {media:.2f}")
    print(f"Maior: {maior}")
    print(f"Menor: {menor}")
    
    return soma, media, maior, menor

def main():
    print("Script Python iniciado")
    
    time.sleep(2)
    
    soma, media, maior, menor = calcular_operacoes()
    
    print("Processamento concluído com sucesso!")
    print(f"Resultado final: {soma}")

if __name__ == "__main__":
    main()