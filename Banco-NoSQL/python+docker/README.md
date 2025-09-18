# Documentando a Atividade de Banco NoSQL - Subindo Python com Docker

Olá! Esta atividade faz parte das minhas disciplinas da graduação de **Tecnólogo em Inteligência Artificial** e tem como objetivo principal a prática com a orquestração de containers. O foco aqui foi pegar uma aplicação simples em Python, utilizando o framework **Flask**, e fazê-la rodar dentro de um container Docker.

---

## Estrutura do Projeto

O projeto é bastante direto, focado em mostrar a integração entre a aplicação, o Dockerfile e o Docker Compose. A estrutura de arquivos é a seguinte:

* **`app.py`**: O arquivo principal da nossa aplicação Flask. [cite_start]Ele cria um servidor web minimalista que exibe a mensagem "Olá, mundo! Esta aplicação está rodando em um container Docker." [cite: 9]
* **`requirements.txt`**: Este arquivo lista as bibliotecas Python que a aplicação precisa para funcionar. [cite_start]No nosso caso, é apenas o **Flask** na versão `2.3.3`[cite: 9].
* **`Dockerfile`**: A "receita" para construir a imagem Docker. Ele me instrui a usar uma imagem base leve do Python, a copiar os arquivos do projeto e a instalar as dependências. [cite_start]Por fim, ele define o comando para iniciar a aplicação[cite: 1, 2, 4, 5, 6, 7, 8].
* **`docker-compose.yml`**: O arquivo que facilita a orquestração do container. Ele define o serviço web, indica onde o Dockerfile está para construir a imagem, e mapeia a porta `5000` do meu host para a porta `5000` do container.

---

## Como Rodar o Projeto

Para executar a aplicação, certifique-se de ter o **Docker** e o **Docker Compose** instalados na sua máquina.

1.  **Clone o repositório:**
    ```bash
    git clone [o-link-do-seu-repositorio]
    cd [pasta-do-projeto]
    ```

2.  **Inicie os containers:**
    No diretório raiz do projeto, execute o seguinte comando no terminal. O Docker Compose irá construir a imagem e iniciar o serviço `web` que definimos no `docker-compose.yml`.
    ```bash
    docker-compose up
    ```
    Eu pude ver a construção da imagem e a aplicação subindo no terminal [Evidência 01].

3.  **Verifique se o container está rodando:**
    Você pode verificar a lista de containers ativos no seu **Docker Desktop** e confirmar que o serviço `pythondocker` está em execução [Evidência 02].

4.  **Acesse a aplicação no navegador:**
    Abra seu navegador e navegue para `http://127.0.0.1:5000`. Você verá a página com a mensagem "Olá, mundo! Esta aplicação está rodando em um container Docker" [Evidência 03].

---

## Considerações Finais

Esta atividade foi um excelente exercício para entender como o Docker simplifica o processo de empacotar e executar aplicações, garantindo que o ambiente de execução seja o mesmo em qualquer lugar. A combinação de Python e Flask com o Docker Compose me permitiu focar no desenvolvimento da aplicação, enquanto o Docker cuidava de todo o ambiente, algo essencial para projetos mais complexos de IA e ciência de dados no futuro.
