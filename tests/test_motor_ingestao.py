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
    url_pokemon = "https://pokeapi.co/api/v2/pokemon/flabebe"
    response = requests.get(url_pokemon)

    assert response.status_code == 200, f"Falha ao buscar dados do Pokémon, status {response.status_code}"

    pokemon_data = response.json()

    resultado = inserir_registro("dados_pokemon", {"dados": pokemon_data})

    assert resultado is not None, "Falha ao inserir dados no Supabase"
    assert resultado.data is not None, "Nenhum dado retornado na inserção"

    print("Teste de inserção bem-sucedido!")