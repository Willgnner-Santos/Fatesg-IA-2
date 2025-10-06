# Teste de Desempenho e Funcionalidades do Redis com Python

Este projeto é um script simples em Python desenvolvido para demonstrar e testar as principais características do Redis, um banco de dados em memória de alto desempenho. O script avalia a velocidade, escalabilidade, flexibilidade de tipos de dados e a baixa latência do Redis, tornando-o um excelente exemplo prático para estudantes e iniciantes em programação.

## 🚀 Objetivos do Projeto

O script foi criado para ilustrar de forma prática os seguintes conceitos do Redis:

-   **Alto Desempenho:** Mede o tempo de execução de operações simples de escrita (`SET`) e leitura (`GET`).
-   **Escalabilidade:** Simula a inserção de múltiplos registros (1000 chaves) para demonstrar como o Redis lida com um volume crescente de dados.
-   **Flexibilidade:** Mostra como armazenar diferentes tipos de estruturas de dados, incluindo:
    -   Strings
    -   Listas (Lists)
    -   Hashes (semelhante a dicionários)
    -   Dados binários (simulados usando codificação Base64)
-   **Baixa Latência:** Realiza leituras sequenciais da mesma chave para exemplificar o uso do Redis como um cache de acesso rápido.

## 🛠️ Tecnologias Utilizadas

-   **Python 3:** Linguagem de programação utilizada para criar o script.
-   **Redis:** Banco de dados em memória.
-   **redis-py:** Biblioteca cliente oficial do Redis para Python.

## 📋 Pré-requisitos

Antes de executar o projeto, você precisará ter o seguinte instalado em sua máquina:

1.  **Python 3:** [Download do Python](https://www.python.org/downloads/)
2.  **Redis:** É necessário ter um servidor Redis rodando localmente.
    -   **Windows:** [Instruções de instalação para Windows (via WSL)](https://redis.io/docs/getting-started/installation/install-redis-on-windows/)
    -   **Linux/macOS:** [Instruções de instalação para Linux/macOS](https://redis.io/docs/getting-started/installation/)
3.  **Biblioteca `redis` para Python.**

## ⚙️ Como Executar o Projeto

Siga os passos abaixo para rodar o script:

1.  **Clone o repositório (ou baixe os arquivos):**
    ```bash
    git clone [https://seu-link-para-o-repositorio.git](https://seu-link-para-o-repositorio.git)
    cd seu-repositorio
    ```

2.  **Instale a biblioteca cliente do Redis para Python:**
    ```bash
    pip install redis
    ```

3.  **Inicie o seu servidor Redis:**
    Abra um terminal separado e inicie o servidor Redis (o comando pode variar um pouco dependendo do seu sistema operacional).
    ```bash
    redis-server
    ```
    Você deverá ver a logo do Redis e mensagens indicando que o servidor está pronto para aceitar conexões.

4.  **Execute o script Python:**
    Abra outro terminal, navegue até a pasta do projeto e execute:
    ```bash
    python teste_redis.py
    ```

## ✅ Resultados Esperados

Ao executar o script, você verá no terminal uma saída similar a esta, demonstrando cada um dos testes realizados:

```
=== Testando Alto Desempenho ===
Valor armazenado: valor_teste
Tempo de execução: 0.00XXXX segundos

=== Testando Escalabilidade ===
Exemplo de valor armazenado: valor_500

=== Testando Flexibilidade ===
String armazenada: Hello Redis!
Lista armazenada: ['item1', 'item2', 'item3']
Hash armazenado: {'campo1': 'valor1', 'campo2': 'valor2'}
Imagem (binário armazenado): aW1hZ2VtX2VtX2JpbmFya... [Cortado]

=== Testando Baixa Latência ===
Cache acessado: config_inicial | Tempo de execução: 0.000139 segundos
Cache acessado: config_inicial | Tempo de execução: 0.000218 segundos
Cache acessado: config_inicial | Tempo de execução: 0.000176 segundos
Cache acessado: config_inicial | Tempo de execução: 0.000171 segundos
Cache acessado: config_inicial | Tempo de execução: 0.000162 segundos

Teste concluído com sucesso!
```

**Observação:** Os tempos de execução podem variar ligeiramente dependendo do hardware da sua máquina, mas devem sempre ser extremamente baixos, evidenciando a performance do Redis.

---

Este projeto é uma ótima forma de ter um primeiro contato prático com o Redis e entender por que ele é tão popular para caching, gerenciamento de sessões, filas e muito mais. Sinta-se à vontade para modificar o código e fazer seus próprios testes!