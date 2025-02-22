#  Ingestão de dados no Supabase

Este projeto implementa um sistema de ingestão de dados que busca informações do Pokémon Flabébé na PokéAPI e insere esses dados no Supabase. O projeto utiliza Python, Poetry e Pytest para garantir uma implementação organizada e testável.

## Estrutura do Projeto

O código está organizado assim

```
ponderadaa/
├── src/
│   ├── ponderadaa/
│   │   ├── __init__.py
│   │   ├── motor_ingestao.py  # Script principal de ingestão
├── tests/
│   ├── __init__.py
│   ├── test_motor_ingestao.py  # Teste automatizado com Pytest
├── .env  # Variáveis de ambiente (Supabase URL e Key)
├── pyproject.toml  # Configuração do Poetry
├── README.md  # Documentação do projeto
```

## Implementação

O código foi feito para ser eficiente, modular e de fácil manutenção. Ele segue boas práticas de desenvolvimento, incluindo uso de variáveis de ambiente, separação de responsabilidades e validação dos dados antes da inserção.

Os dados do Pokémon vem da PokéAPI e os dados são armazenados no Supabase.

### Conexão com Supabase

A conexão com o Supabase é feita utilizando as credenciais armazenadas no `.env`, garantindo segurança e flexibilidade:

```python
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
```

### Função de Ingestão de Dados

A função `inserir_registro` insere os dados obtidos na tabela do Supabase, garantindo que a inserção foi bem-sucedida.

```python
def inserir_registro(tabela: str, dados: dict):
    try:
        resultado = supabase.table(tabela).insert(dados).execute()

        if resultado.data is None:
            raise RuntimeError(f"Falha ao inserir dados na tabela '{tabela}': Nenhuma resposta válida.")

        print(f"Inserção bem-sucedida na tabela '{tabela}': {resultado.data}")
        return resultado
    except Exception as erro:
        print(f"Erro ao inserir na tabela '{tabela}': {erro}")
        return None
```

Esta função:
- Insere os dados no Supabase.
- Verifica se a inserção foi bem-sucedida.
- Lança uma exceção caso a resposta seja inválida.
- Retorna a resposta do banco de dados.

### Busca dos Dados na PokéAPI

Os dados do Pokémon Flabébé são obtidos diretamente da PokéAPI:

```python
import requests

url_pokemon = "https://pokeapi.co/api/v2/pokemon/flabebe"
response = requests.get(url_pokemon)

if response.status_code == 200:
    pokemon_data = response.json()
else:
    raise Exception(f"Erro ao buscar dados: {response.status_code}")

inserir_registro("dados_pokemon", {"dados": pokemon_data})
```

Este código:
- Faz uma requisição HTTP à PokéAPI.
- Garante que a resposta seja `200 OK` antes de processar os dados.
- Insere os dados no Supabase através da função `inserir_registro`.

## Testes Automatizados

Os testes são implementados usando Pytest para garantir que a ingestão de dados ocorra corretamente.

### Arquivo `test_motor_ingestao.py`

```python
import os
import pytest
import requests
from dotenv import load_dotenv
from supabase import create_client, Client
from src.ponderadaa.motor_ingestao import inserir_registro

load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def test_inserir_pokemon():
    """Testa a inserção dos dados do Flabébé no Supabase."""

    url_pokemon = "https://pokeapi.co/api/v2/pokemon/flabebe"
    response = requests.get(url_pokemon)
    assert response.status_code == 200, "Falha ao buscar dados do Pokémon"

    pokemon_data = response.json()
    assert "name" in pokemon_data
    assert "height" in pokemon_data
    assert "weight" in pokemon_data

    resultado = inserir_registro("dados_pokemon", {"dados": pokemon_data})
    assert resultado is not None
    assert resultado.data is not None
    print("Teste de inserção bem-sucedido!")
```

## Como Executar o Projeto

### Instalar Dependências
```bash
poetry install
```

### Configurar as Variáveis de Ambiente

Criar um arquivo `.env` com:

```
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-secreta
```

### Rodar a Ingestão de Dados

```bash
poetry run python src/ponderadaa/motor_ingestao.py
```

### Rodar os Testes

```bash
pytest tests/test_motor_ingestao.py -v
```