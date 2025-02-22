import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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
