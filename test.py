import secrets
import base64
from cryptography.fernet import Fernet
import hmac
import hashlib

def generate_url_safe_key():
    # Générer 32 octets aléatoires
    random_bytes = secrets.token_bytes(32)
    
    # Encoder les octets en base64
    base64_key = base64.urlsafe_b64encode(random_bytes).decode('utf-8')
    
    return base64_key

# Exemple d'utilisation
url_safe_key = generate_url_safe_key()
f = Fernet(url_safe_key)
print(url_safe_key)
t = hmac.new(b'Bd!251673'+b'theo', digestmod=hashlib.sha256).digest()
print(t)
base64_key = base64.urlsafe_b64encode(t).decode('utf-8')
#print(base64_key)

m=base64.urlsafe_b64decode(base64_key)
print(m)
