# importando bibliotecas
import requests
from datetime import datetime
import time
import threading

def obtain_data_API(date):

    # define parâmetros para requisição na API
    params = {
        "symbol": "BTCUSDT",
        "interval": "1d",
        "startTime": int(date.timestamp() * 1000),
        "endTime": int((date.replace(hour=23, minute=59, second=59)).timestamp() * 1000)
    }

    # Realiza a requisição e converte para json
    r = requests.get("https://api.binance.com/api/v3/klines", params=params)
    data = r.json()

    # converte timestamp para datetime
    data[0][0] = datetime.fromtimestamp(data[0][0]/1000)
    return data[0]

def use_memcached(key_value):
    global MEMCACHED
    
    try: # se existir no memcached
        response = MEMCACHED[key_value][1]
        print('Entrada encontrada no MEMCHACHED:\n')
        return response
    except: # se não existir no memcached
        print('Entrada não encontrada no MEMCHACHED. Requisitando...\n')
        MEMCACHED[key_value] = [time.time(), obtain_data_API(key_value)]
        return MEMCACHED[key_value][1]
    
def get_entry(): # espera entrada da data
    global entry, running
    
    while running:
        entry = input("Informe data (ou 'sair'): ")
        if entry.lower() == "sair":
            running = False

def main_loop():
    global entry, running
    
    while running:
        if entry: # se há entrada
            print()
            
            try:
                key_value = datetime.strptime(entry, '%d-%m-%Y') # converte string para datetime
                init_time = time.time() # para medir tempo de processamento
                print(use_memcached(key_value))
                print(f'Tempo de processamento: {(time.time() - init_time)*1000:.2f} milisegundos.')
            except:
                print('Entrada inválida, informe novamente.')
            entry = None  # limpa a variável após uso
            print()

        if len(MEMCACHED)>0: # se existe dados no memcached
            to_del = []
            
            if print_lifes: # exibe memcached
                print('#='*20)
                
            for dict_key in MEMCACHED.keys(): # calcula vida de cada valor
                live = time.time() - MEMCACHED[dict_key][0]

                if print_lifes: # exibe memcached
                    print(f'{dict_key} : {live:.1f} segundos.')
                
                if live > TTL: # adiciona chave em lista para deletar
                    to_del.append(dict_key)

            if to_del: # se existe chaves para serem deletadas, deleta
                for deleting in to_del:
                    del MEMCACHED[deleting]

            if print_lifes: # exibe memcached
                print('#='*20)

        time.sleep(1)

while True: # recebe valor do TTL
    TTL = input('Informe o TTL (segundos): ')
    try:
        TTL = int(TTL)
        break
    except:
        print('Entrada inválida.')

while True: # recebe se usuário quer exibir memcached
    print_lifes = input('Deseja exibir as vidas do TTL? S/n: ')
    if print_lifes.lower() == 's':
        print_lifes = True
        break
    elif print_lifes.lower() == 'n':
        print_lifes = False
        break
    else:
        print('Entrada inválida.')
print()

entry = None
running = True
MEMCACHED = {}

# cria e inicia a thread para o input
thread_input = threading.Thread(target=get_entry, daemon=True)
thread_input.start()

# executa o loop principal
main_loop()

print("Programa encerrado.")
time.sleep(5)