from models.vault import Vault
from getpass import getpass
vault = Vault()
print("=== Mon Coffre ===")
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
    print("\n--- MENU ---")
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
