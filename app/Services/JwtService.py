from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from Config.Settings import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY


class JwtService:
    """Handles creating and validating JWT access tokens."""

    @staticmethod
    def create_access_token(user_id: int) -> str:
        """Build a signed token for the given user ID."""
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload = {"sub": str(user_id), "exp": expire}
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict:
        """
        Decode and validate a token.
        Raises JWTError if the token is invalid or expired.
        """
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    @staticmethod
    def get_user_id_from_token(token: str) -> int:
        """Extract the user ID (sub claim) from a valid token."""
        payload = JwtService.decode_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise JWTError("Token missing user id")
        return int(user_id)
