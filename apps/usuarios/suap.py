import os

from authlib.integrations.django_client import OAuth
from dotenv import load_dotenv

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