import jwt
from jwt import PyJWKClient
from app.config import settings

JWKS_URL = f"{settings.supabase_url}/auth/v1/.well-known/jwks.json"
jwks_client = PyJWKClient(JWKS_URL)

def verify_token(token: str) -> dict:
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["ES256"],
            audience="authenticated",
        )
        return payload
    except jwt.PyJWTError as e:
        raise ValueError(f"Token invalide : {e}")