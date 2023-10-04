import os
import getpass
from cryptography.fernet import Fernet
import hashlib
import base64
import hmac

# Chemin du fichier contenant la clé de l'utilisateur
user_key_file = "user_key.key"

# Fonction pour générer la clé de l'application à partir du mot de passe de l'utilisateur
def generate_app_key(user_password, user_key):
    # Combinez le mot de passe de l'utilisateur et la clé de l'utilisateur
    combined_key = user_password.encode() + user_key.encode()

    # Utilisez HMAC pour générer une clé de 32 octets
    app_key = hmac.new(combined_key, digestmod=hashlib.sha256).digest()

    # Convertissez la clé en base64
    app_key_base64 = base64.urlsafe_b64encode(app_key).decode('utf-8')

    return app_key_base64

# Fonction pour déchiffrer un fichier
def decrypt_file(file_path, app_key, user_key):
    with open(file_path, "rb") as file:
        data = file.read()

    c = hmac.new(user_key.encode()+app_key.encode(), digestmod=hashlib.sha256).digest()
    
    # Déchiffrement avec la clé de l'utilisateur
    fernet_user = Fernet(base64.urlsafe_b64encode(c).decode('utf-8'))
    decrypted_data = fernet_user.decrypt(data)
    
    # Déchiffrement avec la clé de l'application
    fernet_app = Fernet(app_key)
    decrypted_data = fernet_app.decrypt(decrypted_data)

    return decrypted_data

# Chemin où sont stockées les données chiffrées
data_folder = "data_folder"

# Demandez le mot de passe de l'utilisateur
user_password = getpass.getpass("Entrez votre mot de passe : ")


with open(user_key_file, "r") as file:
    user_key = file.read()

# Convertissez la clé de l'application en bytes
app_key = generate_app_key(user_password, user_key)

# Liste des fichiers chiffrés
encrypted_files = os.listdir(data_folder)

# Décryptez chaque fichier et enregistrez-le
for encrypted_file in encrypted_files:
    if 'decrypted' not in encrypted_file:
        encrypted_file_path = os.path.join(data_folder, encrypted_file)
        decrypted_data = decrypt_file(encrypted_file_path, app_key, user_key)

        # Enregistrez les données déchiffrées dans un nouveau fichier
        decrypted_file_path = os.path.join(data_folder, "decrypted_" + encrypted_file)
        with open(decrypted_file_path, "wb") as file:
            file.write(decrypted_data)

print("Les fichiers ont été déchiffrés avec succès.")
