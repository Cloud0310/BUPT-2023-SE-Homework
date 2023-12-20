import base64

import rsa
from rsa import VerificationError



def check_csrf_token(requests):
    csrf_token = requests.headers.get("X-CSRF-Token")

    return 1


def verify_signature(verify_str, public_key, signature):
    public_key_parsed = rsa.PublicKey.load_pkcs1_openssl_pem(
        (
            "-----BEGIN PUBLIC KEY-----\n" + public_key + "\n-----END PUBLIC KEY-----"
        ).encode()
    )
    try:
        rsa.verify(
            verify_str.encode(),
            base64.urlsafe_b64decode(signature.encode()),
            public_key_parsed,
        )
        return True
    except VerificationError:
        return False
