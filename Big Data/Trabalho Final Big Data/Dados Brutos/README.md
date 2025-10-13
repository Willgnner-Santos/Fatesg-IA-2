# Dataset Bruto de E-commerce para Análise de Dados

## 1. Descrição Geral

Esta pasta contém o conjunto de dados brutos utilizados para um projeto de pipeline de dados end-to-end. O dataset simula as operações de uma plataforma de e-commerce, abrangendo informações de clientes, produtos, pedidos e avaliações.

O volume total dos dados é de aproximadamente **3 GB**, com a tabela de itens de pedido (`order_items.csv`) contendo **40 milhões de registros**. A escala e a estrutura relacional destes dados foram a base para a construção de uma solução de análise com ferramentas de Big Data.

## 2. Conteúdo da Pasta

Esta pasta contém os seguintes 5 arquivos em formato `.csv`:

* `customers.csv`: Contém informações demográficas e de cadastro de cada cliente.
* `products.csv`: Contém o catálogo de produtos, incluindo categoria, marca e preço.
* `orders.csv`: Contém o registo de cada pedido realizado, incluindo data, valor total e cliente associado.
* `order_items.csv`: A tabela mais granular, contendo cada item individual dentro de cada pedido.
* `product_reviews.csv`: Contém as avaliações (nota e texto) feitas pelos clientes para produtos específicos.

## 3. Dicionário de Dados

A seguir, a estrutura detalhada de cada tabela.

### Customers
* `customer_id` (int): Identificador único de cada cliente.
* `name` (string): Nome completo do cliente.
* `email` (string): Endereço de e-mail do cliente.
* `gender` (string): Género do cliente ('Male', 'Female', 'Other').
* `signup_date` (date): Data de registo do cliente.
* `country` (string): País de residência do cliente.

### Products
* `product_id` (int): Identificador único de cada produto.
* `product_name` (string): Nome do produto.
* `category` (string): Categoria do produto.
* `price` (float): Preço por unidade.
* `stock_quantity` (int): Quantidade disponível em stock.
* `brand` (string): Marca do produto.

### Orders
* `order_id` (int): Identificador único de cada pedido.
* `customer_id` (int): ID do cliente que fez o pedido (chave estrangeira para Customers).
* `order_date` (date): Data em que o pedido foi feito.
* `total_amount` (float): Valor total do pedido.
* `payment_method` (string): Método de pagamento utilizado.
* `shipping_country` (string): País para onde o pedido é enviado.

### Order Items
* `order_item_id` (int): Identificador único de cada item de pedido.
* `order_id` (int): ID do pedido a que este item pertence (chave estrangeira para Orders).
* `product_id` (int): ID do produto encomendado (chave estrangeira para Products).
* `quantity` (int): Número de unidades encomendadas.
* `unit_price` (float): Preço por unidade no momento do pedido.

### Product Reviews
* `review_id` (int): Identificador único de cada avaliação.
* `product_id` (int): ID do produto avaliado (chave estrangeira para Products).
* `customer_id` (int): ID do cliente que escreveu a avaliação (chave estrangeira para Customers).
* `rating` (int): Pontuação da avaliação (1 a 5).
* `review_text` (string): Conteúdo textual da avaliação.
* `review_date` (date): Data em que a avaliação foi escrita.

## 4. Natureza dos Dados

Este é um **dataset sintético**, gerado artificialmente para fins educacionais e de desenvolvimento. A estrutura, os tipos de dados e os relacionamentos são realistas, mas os valores de texto (nomes, e-mails, etc.) são placeholders e não representam pessoas ou produtos reais.

## 5. Fonte dos Dados

O dataset original está publicamente disponível na plataforma Kaggle e pode ser acedido através do seguinte link:

* **Fonte:** [Synthetic E-commerce Relational Dataset - Kaggle](https://www.kaggle.com/datasets/naelaqel/synthetic-e-commerce-relational-dataset?resource=download)
