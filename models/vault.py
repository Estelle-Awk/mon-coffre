import json, os
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
