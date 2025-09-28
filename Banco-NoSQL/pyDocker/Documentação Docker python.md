# Documentação - Containerização de Aplicação Python com Docker

## Objetivo
Este tutorial demonstra o processo completo de containerização de uma aplicação Python usando Docker, desde a criação dos arquivos de configuração até a execução do container.

## Ambiente de Desenvolvimento
- **Sistema Operacional**: Windows com Docker Desktop
- **Ferramenta**: Docker Desktop Personal
- **Python**: Versão 3.13.7 (via imagem oficial)
- **Interface**: Docker Desktop GUI

## Estrutura do Projeto

### Arquivos Criados

```
projeto/
├── testeTarefa.py        # Aplicação Python principal
├── Dockerfile            # Instruções para construção da imagem
└── docker-compose.yml    # Configuração de orquestração
```

## Implementação dos Arquivos

### 1. Aplicação Python (testeTarefa.py)

```python
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
```

**Características da aplicação:**
- Gera 10 números aleatórios entre 1 e 100
- Calcula soma, média, maior e menor valor
- Inclui delay de 2 segundos para simular processamento
- Exibe resultados formatados no console

### 2. Dockerfile

```dockerfile
FROM python:3.13.7

WORKDIR /app

COPY testeTarefa.py .

CMD ["python", "testeTarefa.py"]
```

**Explicação das instruções:**
- `FROM python:3.13.7`: Usa imagem oficial do Python versão 3.13.7
- `WORKDIR /app`: Define `/app` como diretório de trabalho no container
- `COPY testeTarefa.py .`: Copia o script Python para dentro do container
- `CMD ["python", "testeTarefa.py"]`: Comando executado quando o container iniciar

### 3. Docker Compose (docker-compose.yml)

```yaml
version: '3.8'

services:
  python-script:
    build: .
    container_name: teste-python-script
```

**Configurações definidas:**
- `version: '3.8'`: Versão do Docker Compose
- `python-script`: Nome do serviço
- `build: .`: Constrói a imagem a partir do Dockerfile no diretório atual
- `container_name`: Nome específico para o container

## Processo de Construção e Execução

### 1. Build da Imagem

A imagem foi construída automaticamente através do Docker Desktop quando o projeto foi adicionado à interface.

**Processo realizado:**
1. Leitura do Dockerfile
2. Download da imagem base `python:3.13.7`
3. Criação do diretório de trabalho `/app`
4. Cópia do arquivo `testeTarefa.py`
5. Definição do comando de execução

**Resultado:**
- **Nome da imagem**: `meu-script`
- **Tag**: `latest`
- **Image ID**: `26018dc59fb2`
- **Tamanho**: 1.6 GB

### 2. Execução do Container

O container foi executado através da interface do Docker Desktop:

**Configuração de execução:**
- **Nome do container**: `thirsty_ptolemy` (gerado automaticamente)
- **Status**: Exited (0) - Execução bem-sucedida
- **Duração**: Aproximadamente alguns segundos

## Resultados da Execução

### Output do Script Python

**Logs capturados:**
```
Script Python iniciado
Iniciando processamento...
Números gerados: [61, 79, 54, 36, 28, 73, 99, 34, 14, 97]
Soma: 575
Media: 57.50
Maior: 99
Menor: 14
Processamento concluído com sucesso!
Resultado final: 575
```

### Análise dos Resultados

| Métrica | Valor | Observação |
|---------|-------|------------|
| Números gerados | 10 valores | Entre 1 e 100 como esperado |
| Soma total | 575 | Cálculo correto |
| Média | 57.50 | Precisão de 2 casas decimais |
| Maior valor | 99 | Identificação correta |
| Menor valor | 14 | Identificação correta |
| Status de saída | 0 | Execução sem erros |

## Gerenciamento via Docker Desktop

### Interface Utilizada

**Seções acessadas:**
1. **Images**: Para visualizar a imagem construída
2. **Containers**: Para executar e monitorar o container
3. **Logs**: Para verificar a saída da aplicação

### Funcionalidades Utilizadas

**Ações realizadas:**
-  **Run**: Iniciar o container
-  **Logs**: Visualizar output da aplicação
-  **Delete**: Possibilidade de remoção (não utilizada)
-  **Restart**: Reiniciar container se necessário

## Vantagens da Containerização Observadas

### 1. Portabilidade
- Aplicação roda em qualquer sistema com Docker
- Independência do ambiente Python local

### 2. Isolamento
- Container executado em ambiente isolado
- Sem interferência com sistema host

### 3. Reprodutibilidade
- Mesmos resultados em diferentes execuções
- Ambiente consistente e versionado

### 4. Simplicidade
- Dockerfile minimalista mas eficaz
- Docker Compose facilita o gerenciamento

## Características Técnicas

### Recursos do Container

**Configurações padrão:**
- CPU: Compartilhada com host
- RAM: Sem limite específico definido
- Storage: Ephemeral (dados não persistem)
- Network: Bridge padrão

## Casos de Uso da Aplicação

### 1. Processamento de Dados
- Análise estatística básica
- Geração de relatórios numéricos

### 2. Testes de Performance
- Benchmark de operações matemáticas
- Verificação de ambiente containerizado

### 3. Demonstração Educacional
- Exemplo prático de containerização
- Introdução ao Docker com Python

## Conclusão

O projeto demonstra como uma aplicação Python simples pode ser facilmente containerizada e executada de forma consistente, estabelecendo uma base sólida para aplicações mais complexas e deployments em produção.
