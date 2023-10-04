import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import getpass
import shutil
import zipfile
from cryptography.fernet import Fernet
import hashlib
import base64
import hmac

# Chemin où seront stockés les fichiers chiffrés
data_folder = "data_folder"
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

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

# Fonction pour chiffrer un fichier
def encrypt_file(file_path, app_key, user_key):
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
    encrypted_file_path = os.path.join(data_folder, os.path.basename(file_path))
    with open(encrypted_file_path, "wb") as file:
        file.write(encrypted_data)

# Fonction pour sélectionner les fichiers à chiffrer
def select_files():
    file_paths = filedialog.askopenfilenames()
    if file_paths:
        for file_path in file_paths:
            encrypt_file(file_path, app_key, user_key)
        messagebox.showinfo("Chiffrement terminé", "Les fichiers ont été chiffrés avec succès.")

# Créez une fenêtre Tkinter
root = tk.Tk()
root.title("Application de chiffrement de fichiers")

# Demandez le mot de passe de l'utilisateur
user_password = getpass.getpass("Entrez votre mot de passe : ")

# Générez la clé de l'application
if not os.path.exists(user_key_file):
    user_key = getpass.getpass("Créez votre clé utilisateur : ")
    with open(user_key_file, "w") as file:
        file.write(user_key)
else:
    with open(user_key_file, "r") as file:
        user_key = file.read()

# Convertissez la clé de l'application en bytes
app_key = generate_app_key(user_password, user_key)

# Créez un bouton pour sélectionner les fichiers à chiffrer
select_button = tk.Button(root, text="Sélectionner les fichiers à chiffrer", command=select_files)
select_button.pack()

root.mainloop()