import bcrypt


class PasswordHasher:
    """Class to hash and verify passwords using bcrypt."""

    @staticmethod
    def hash_password(password: str, rounds: int = 12) -> str:
        if not isinstance(password, str):
            raise TypeError("password must be str")
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=rounds))
        return hashed.decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        if not all(isinstance(x, str) for x in (password, hashed)):
            raise TypeError("password and hashed must be str")
        try:
            return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
        except (ValueError, TypeError):
            return False
