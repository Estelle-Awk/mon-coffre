import os

os.makedirs("models", exist_ok=True)
os.makedirs("data", exist_ok=True)

open("models/crypto.py","w",encoding="utf-8").write('''import hashlib
import base64
class Crypto:
    @staticmethod
    def hash_master(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    @staticmethod
    def derive_key(password: str) -> bytes:
        return hashlib.sha256(password.encode()).digest()
    @staticmethod
    def encrypt(text: str, password: str) -> str:
        key = Crypto.derive_key(password)
        text_bytes = text.encode()
        encrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(text_bytes)])
        return base64.b64encode(encrypted).decode()
    @staticmethod
    def decrypt(enc_text: str, password: str) -> str:
        key = Crypto.derive_key(password)
        enc_bytes = base64.b64decode(enc_text.encode())
        decrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(enc_bytes)])
        return decrypted.decode()
''')

open("models/entry.py","w",encoding="utf-8").write('''from datetime import datetime
class PasswordEntry:
    def __init__(self, site, username, password_encrypted, note=""):
        self.site = site
        self.username = username
        self.password_encrypted = password_encrypted
        self.note = note
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    def to_dict(self):
        return self.__dict__
    @staticmethod
    def from_dict(data):
        e = PasswordEntry(data['site'], data['username'], data['password_encrypted'], data.get('note',''))
        e.created_at = data.get('created_at','')
        return e
''')

open("models/vault.py","w",encoding="utf-8").write('''import json, os
from .entry import PasswordEntry
from .crypto import Crypto
from collections import deque
class Vault:
    def __init__(self):
        self.master_hash_file = "data/master.hash"
        self.vault_file = "data/vault.json"
        self.entries = []
        self.history = []
        self.search_queue = deque()
    def master_exists(self):
        return os.path.exists(self.master_hash_file)
    def set_master(self, password):
        os.makedirs("data", exist_ok=True)
        h = Crypto.hash_master(password)
        with open(self.master_hash_file, "w") as f:
            f.write(h)
    def check_master(self, password):
        if not self.master_exists(): return False
        with open(self.master_hash_file, "r") as f:
            return f.read() == Crypto.hash_master(password)
    def load(self, master_password):
        if not os.path.exists(self.vault_file):
            self.entries = []
            return
        try:
            with open(self.vault_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.entries = [PasswordEntry.from_dict(d) for d in data]
        except:
            self.entries = []
    def save(self):
        os.makedirs("data", exist_ok=True)
        with open(self.vault_file, "w", encoding="utf-8") as f:
            json.dump([e.to_dict() for e in self.entries], f, indent=2)
    def add(self, site, username, password_clair, master_password, note=""):
        enc = Crypto.encrypt(password_clair, master_password)
        entry = PasswordEntry(site, username, enc, note)
        self.entries.append(entry)
        self.history.append(f"Ajout {site}")
        self.save()
        return entry
    def get_password(self, entry, master_password):
        return Crypto.decrypt(entry.password_encrypted, master_password)
''')

open("main.py","w",encoding="utf-8").write('''from models.vault import Vault
from getpass import getpass
vault = Vault()
print("=== PASSLOCKER ===")
if not vault.master_exists():
    print("Premiere utilisation, cree ton mot de passe maitre.")
    p1 = getpass("Nouveau mot de passe maitre: ")
    vault.set_master(p1)
    master = p1
    print("Maitre cree !")
else:
    master = getpass("Mot de passe maitre: ")
    if not vault.check_master(master):
        print("Incorrect"); exit()
vault.load(master)
while True:
    print("\\n--- MENU ---")
    print(f"Entrees: {len(vault.entries)}")
    print("1. Ajouter  2. Voir tout  3. Voir un mot de passe  0. Quitter")
    c = input("Choix: ")
    if c=="1":
        site=input("Site: "); user=input("Username: "); pwd=getpass("Pass du site: ")
        vault.add(site,user,pwd,master); print("Ajoute !")
    elif c=="2":
        [print(f"{i} | {e.site} | {e.username}") for i,e in enumerate(vault.entries)]
    elif c=="3":
        try:
            idx=int(input("Numero: ")); e=vault.entries[idx]
            print(f"Pass: {vault.get_password(e,master)}")
        except: print("Erreur")
    elif c=="0": break
''')

open("README.md","w",encoding="utf-8").write("# PassLocker - IFRI L2\\nGestionnaire de mots de passe local")
open("requirements.txt","w").write("")
open("data/.gitkeep","w").write("")

print("PROJET CREE AVEC SUCCES ! Maintenant lance: python main.py")