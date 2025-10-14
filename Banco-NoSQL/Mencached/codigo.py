import time
import random

# Cache simples
cache = {}
TTL = 5  # tempo de vida em segundos

# Armazena o valor e calcula horário de expiração
momento_criacao = time.time()
cache["chave_exemplo"] = random.randint(1,100)
hora_criacao = time.strftime("%H:%M:%S", time.localtime(momento_criacao))
hora_expiracao = time.strftime("%H:%M:%S", time.localtime(momento_criacao + TTL))

print(f"\nValor armazenado às {hora_criacao}")
print(f"Expira automaticamente às {hora_expiracao} (TTL = {TTL}s)")

# Mostra o cache antes da expiração
print("\nEstado do cache antes da expiração:")
print(cache)

# Leitura imediata
print("\nLeitura imediata:", cache.get("chave_exemplo"))

# Aguarda 6 segundos
time.sleep(6)

# Verifica se expirou
if "chave_exemplo" in cache:
    # Se o tempo passou, remove automaticamente
    if time.time() - momento_criacao >= TTL:
        del cache["chave_exemplo"]
        print("\nO valor expirou e foi removido automaticamente.")
    else:
        print("\nO valor ainda está disponível:", cache["chave_exemplo"])
else:
    print("\nO valor já foi removido.")

# Mostra o cache após a expiração
print(f"\nEstado do cache depois da expiração: {cache}\n")