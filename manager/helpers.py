import secrets


RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def random_password(length, allowed_chars=RANDOM_STRING_CHARS):
    return "".join(secrets.choice(allowed_chars) for i in range(length))