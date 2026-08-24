import os

from authlib.integrations.django_client import OAuth
from dotenv import load_dotenv

load_dotenv()

oauth = OAuth()

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": (
            "openid email profile "
            "https://www.googleapis.com/auth/classroom.courses.readonly "
            "https://www.googleapis.com/auth/classroom.coursework.me.readonly"
        )
    },
)

def obter_turmas(token):
    resposta = oauth.google.get(
        "https://classroom.googleapis.com/v1/courses",
        token=token,
        params={
            "courseStates": "ACTIVE"
        }
    )

    resposta.raise_for_status()

    return resposta.json()

def obter_atividades(token, curso_id):
    resposta = oauth.google.get(
        f"https://classroom.googleapis.com/v1/courses/{curso_id}/courseWork",
        token=token,
        params={
            "courseWorkStates": "PUBLISHED"
        }
    )

    resposta.raise_for_status()

    return resposta.json()