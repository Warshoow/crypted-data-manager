from tkinter import simpledialog
from tkinter import messagebox
import os
import hashlib
import base64
import hmac
from interface import AppInterface
from encrypt import Encrypt
from decrypt import Decrypt


# Chemin où seront stockés les fichiers chiffrés
crypt_folder = ''
decrypt_folder = ''

conf_file = 'app.conf'
if not os.path.exists(conf_file):
    path_crypt = simpledialog.askstring('Information', 'Entrez le path de destination des fichier crypté (drive)')
    path_decrypt = simpledialog.askstring('Information', 'Entrez le path de destination des fichier décrypté')
    with open(conf_file, "w") as file:
        file.write(path_crypt)
        file.write(';')
        file.write(path_decrypt)

with open(conf_file, 'r') as file:
    paths = file.read().split(';')
    crypt_folder = paths[0]
    decrypt_folder = paths[1]

# Chemin du fichier contenant la clé de l'utilisateur
user_key_file = "user_key.key"

selected_files = []
encrypted_files = [] 


# Fonction pour générer la clé de l'application à partir du mot de passe de l'utilisateur
def generate_app_key(user_password, user_key):
    # Combinez le mot de passe de l'utilisateur et la clé de l'utilisateur
    combined_key = user_password.encode() + user_key.encode()

    # Utilisez HMAC pour générer une clé de 32 octets
    app_key = hmac.new(combined_key, digestmod=hashlib.sha256).digest()

    # Convertissez la clé en base64
    app_key_base64 = base64.urlsafe_b64encode(app_key).decode('utf-8')

    return app_key_base64

def clickEncryption():
    encrypt.encrypt_selected_files(selected_files)
    selected_files.clear()
    app.delete_file_listbox(app.file_listbox)
    app.delete_file_listbox(app.encrypted_listbox)
    refreshCryptedFile()

def selectingFiles():
    app.select_files(selected_files)

def refreshCryptedFile():
    encrypted_files = decrypt.get_crypted_file_list()
    app.update_file_listbox(app.encrypted_listbox, encrypted_files)

def clickDecryption():
    if len(app.encrypted_listbox.curselection()) < 1:
        messagebox.showwarning("Aucun fichier sélectionné", "Veuillez sélectionner des fichiers à déchiffrer.")
    for item_index in app.encrypted_listbox.curselection():
        file_to_decrypt = app.encrypted_listbox.get(item_index)
        decrypt.register_decrypted_file(file_to_decrypt)

app = AppInterface("Application de chiffrement de fichiers")


# Demandez le mot de passe de l'utilisateur
user_password = simpledialog.askstring('Information', 'Entrez votre mot de passe', show='*')

# Générez la clé de l'application
if not os.path.exists(user_key_file):
    user_key = simpledialog.askstring('Information', 'Créez votre clé utilisateur')
    with open(user_key_file, "w") as file:
        file.write(user_key)
else:
    with open(user_key_file, "r") as file:
        user_key = file.read()


app_key = generate_app_key(user_password, user_key)
encrypt = Encrypt(crypt_folder, app_key, user_key)
decrypt = Decrypt(decrypt_folder, app_key, user_key)


app.button('Sélectionner les fichiers à chiffrer', selectingFiles)
app.listbox()

refreshCryptedFile()

app.button('Chiffrer les fichiers sélectionnés', clickEncryption)
app.button('Déchiffrer les fichiers sélectionnés', clickDecryption)

app.run()
