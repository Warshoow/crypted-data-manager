from cryptography.fernet import Fernet
import hashlib
import hmac
import base64
import os
from tkinter import messagebox

class Decrypt:
    def __init__(self, path, app_key, user_key):
        self.path = path
        self.app_key = app_key
        self.user_key = user_key

    def decrypt_file(self, file_path):
        with open(file_path, "rb") as file:
            data = file.read()

        c = hmac.new(self.user_key.encode()+self.app_key.encode(), digestmod=hashlib.sha256).digest()
        
        # Déchiffrement avec la clé de l'utilisateur
        fernet_user = Fernet(base64.urlsafe_b64encode(c).decode('utf-8'))
        decrypted_data = fernet_user.decrypt(data)
        
        # Déchiffrement avec la clé de l'application
        fernet_app = Fernet(self.app_key)
        decrypted_data = fernet_app.decrypt(decrypted_data)

        return decrypted_data

    def get_crypted_file_list(self):
        encrypted_files = os.listdir(self.path)
        cryted_list = []
        for encrypted_file in encrypted_files:
            if 'decrypted' not in encrypted_file:
                cryted_list.append(os.path.join(self.path, encrypted_file))
        return cryted_list

    
    def register_decrypted_file(self, encrypted_file):
        if 'decrypted' not in encrypted_file:
            encrypted_file_path = os.path.join(self.path, encrypted_file)
            decrypted_data = self.decrypt_file(encrypted_file_path)
            decrypted_file_path = os.path.join(self.path, "decrypted_" + encrypted_file)
            with open(decrypted_file_path, "wb") as file:
                file.write(decrypted_data)
            messagebox.showinfo("Déchiffrement terminé", "Les fichiers ont été déchiffrés avec succès.")