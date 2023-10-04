from cryptography.fernet import Fernet
import hashlib
import hmac
import base64
import os
from tkinter import messagebox

class Encrypt:
    def __init__(self, path, app_key, user_key):
        self.path = path
        self.app_key = app_key
        self.user_key = user_key

    def encrypt_file(self, file_path, app_key, user_key):
        with open(file_path, "rb") as file:
            data = file.read()

        # Chiffrement avec la clé de l'application
        fernet_app = Fernet(app_key)
        encrypted_data = fernet_app.encrypt(data)

        c = hmac.new(user_key.encode()+app_key.encode(), digestmod=hashlib.sha256).digest()

        # Chiffrement avec la clé de l'utilisateur
        fernet_user = Fernet(base64.urlsafe_b64encode(c).decode('utf-8'))
        encrypted_data = fernet_user.encrypt(encrypted_data)

        # Enregistrez les données chiffrées dans le dossier de données
        encrypted_file_path = os.path.join(self.path, os.path.basename(file_path))
        with open(encrypted_file_path, "wb") as file:
            file.write(encrypted_data)


    def encrypt_selected_files(self, selected_files):
        if selected_files:
            for file_path in selected_files:
                self.encrypt_file(file_path, self.app_key, self.user_key)
            messagebox.showinfo("Chiffrement terminé", "Les fichiers ont été chiffrés avec succès.")
            return True
        else:
            messagebox.showwarning("Aucun fichier sélectionné", "Veuillez sélectionner des fichiers à chiffrer.")
            return False