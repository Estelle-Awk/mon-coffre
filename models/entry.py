from datetime import datetime
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
