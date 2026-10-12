from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

from .config import settings

config = Config(".env")

oauth = OAuth(config)

oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    # server_metadata_url=settings.GOOGLE_AUTH_URL,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile",
        # "response_type": "code",
    },
)


def main():
    print(dir(oauth.config))


if __name__ == "__main__":
    main()
