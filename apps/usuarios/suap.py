import os

from authlib.integrations.django_client import OAuth
from dotenv import load_dotenv

from datetime import datetime

load_dotenv()

oauth = OAuth()

oauth.register(
    name="suap",
    client_id=os.getenv("SUAP_CLIENT_ID"),
    client_secret=os.getenv("SUAP_CLIENT_SECRET"),
    api_base_url="https://suap.ifrn.edu.br/api/",
    access_token_url="https://suap.ifrn.edu.br/o/token/",
    authorize_url="https://suap.ifrn.edu.br/o/authorize/",
)

def obter_periodo_atual(token):
    ano_atual = datetime.now().year
    hoje = datetime.now().date()

    anos = [ano_atual, ano_atual - 1]

    for ano in anos:
        resposta = oauth.suap.get(
            f"ensino/meu-calendario-academico/{ano}/1/",
            token=token
        )

        if resposta.status_code != 200:
            continue

        calendario = resposta.json()

        data_inicio = datetime.strptime(
            calendario["data_inicio"],
            "%d/%m/%Y"
        ).date()

        data_fim = datetime.strptime(
            calendario["data_fim"],
            "%d/%m/%Y"
        ).date()

        if data_inicio <= hoje <= data_fim:
            return f"{ano}.1"

    return None

def obter_diarios(token):
    periodo = obter_periodo_atual(token)

    if not periodo:
        return []

    resposta = oauth.suap.get(
        f"ensino/diarios/{periodo}/",
        token=token
    )

    resposta.raise_for_status()

    return resposta.json()