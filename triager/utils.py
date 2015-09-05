import hashlib


def hash_pwd(password):
    return hashlib.sha512(password).hexdigest()
