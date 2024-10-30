from library import *

# Hash a password using MD5
def hash_password(password):
    # Encode the password to bytes, then hash with MD5
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    return hashed_password