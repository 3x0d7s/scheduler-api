import os

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import BearerTransport, AuthenticationBackend, JWTStrategy

from src.auth.manager import get_user_manager
from src.users.models import User

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    from dotenv import load_dotenv

    load_dotenv()

    secret = os.environ.get("SECRET_KEY")

    return JWTStrategy(secret=secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)