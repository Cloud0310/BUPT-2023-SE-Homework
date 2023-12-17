from rsa import VerificationError
import base64
import rsa

"""
Hint: utils.py is a file that contains all the utility functions for the app.
"""

def generate_timestamp_id():
    random_shuffled = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return "".join(random_shuffled[i] for i in range(32))


# Generate a timestamp id
def verify_signature(verify_str, public_key, signature): 
    public_key_parsed = rsa.PublicKey.load_pkcs1_openssl_pem(("-----BEGIN PUBLIC KEY-----\n" + public_key + "\n-----END PUBLIC KEY-----").encode())
    try:
        rsa.verify(verify_str.encode(), base64.urlsafe_b64decode(signature.encode()), public_key_parsed)
        return True
    except VerificationError:
        return False


# Check if the csrf token is valid
def check_csrf_token(requests):
    csrf_token = requests.headers.get("X-CSRF-Token")
    print("CSRF_TOKEN: ", csrf_token)
    return 1