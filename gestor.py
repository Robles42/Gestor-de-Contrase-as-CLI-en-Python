import os
import secrets
import string
import hashlib
from cryptography.fernet import Fernet
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

class PasswordManager:
    def __init__(self, key_path="master.key", data_path="passwords.dat", master_pw_hash="master.hash"):
        self.key_path = key_path
        self.data_path = data_path
        self.master_pw_hash = master_pw_hash
        self.key = self.load_key()
        self.cipher = Fernet(self.key)

    def load_key(self):
        if not os.path.exists(self.key_path):
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as key_file:
                key_file.write(key)
            return key
        return open(self.key_path, "rb").read()

    def check_master_pw(self):
        if not os.path.exists(self.master_pw_hash):
            console.print("[bold yellow]Configuración Inicial:[/bold yellow] Crea tu Master Password.")
            pw = Prompt.ask("Nueva Master Password", password=True)
            h = hashlib.sha256(pw.encode()).hexdigest()
            with open(self.master_pw_hash, "w") as f:
                f.write(h)
            return True
        
        pw = Prompt.ask("Introduce tu Master Password", password=True)
        h = hashlib.sha256(pw.encode()).hexdigest()
        with open(self.master_pw_hash, "r") as f:
            stored_h = f.read().strip()
        return h == stored_h

    def add_password(self, site, password):
        encrypted_pw = self.cipher.encrypt(password.encode()).decode()
        with open(self.data_path, "a") as f:
            f.write(f"{site}|{encrypted_pw}\n")
        console.print(f"[bold green]✔ Guardado con éxito.[/bold green]")

    def delete_password(self, site_to_delete):
        if not os.path.exists(self.data_path): return
        
        lines = []
        found = False
        with open(self.data_path, "r") as f:
            lines = f.readlines()
        
        with open(self.data_path, "w") as f:
            for line in lines:
                site, _ = line.strip().split("|")
                if site.lower() != site_to_delete.lower():
                    f.write(line)
                else:
                    found = True
        
        if found:
            console.print(f"[bold red]✘ Registro de {site_to_delete} eliminado.[/bold red]")
        else:
            console.print(f"[yellow]No se encontró el sitio: {site_to_delete}[/yellow]")

    def list_passwords(self):
        if not os.path.exists(self.data_path) or os.stat(self.data_path).st_size == 0:
            console.print("[yellow]La base de datos está vacía.[/yellow]")
            return

        table = Table(title="Panel de Credenciales")
        table.add_column("Sitio/Servicio", style="cyan")
        table.add_column("Password Descifrada", style="magenta")

        with open(self.data_path, "r") as f:
            for line in f:
                site, enc_pw = line.strip().split("|")
                dec_pw = self.cipher.decrypt(enc_pw.encode()).decode()
                table.add_row(site, dec_pw)
        console.print(table)

def generar_password(longitud=20):
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

def main():
    manager = PasswordManager()
    if not manager.check_master_pw():
        console.print("[bold red]Acceso Denegado.[/bold red]")
        return

    while True:
        console.print("\n[bold cyan]PyLock CLI[/bold cyan] | 1:Añadir | 2:Generar | 3:Ver | 4:Borrar | 5:Salir")
        choice = Prompt.ask("Acción", choices=["1", "2", "3", "4", "5"])

        if choice == "1":
            s = Prompt.ask("Sitio")
            p = Prompt.ask("Password", password=True)
            manager.add_password(s, p)
        elif choice == "2":
            s = Prompt.ask("Sitio")
            l = int(Prompt.ask("Longitud", default="20"))
            pw = generar_password(l)
            console.print(f"Password: [bold white on blue] {pw} [/bold white on blue]")
            manager.add_password(s, pw)
        elif choice == "3":
            manager.list_passwords()
        elif choice == "4":
            s = Prompt.ask("Nombre del sitio a borrar")
            manager.delete_password(s)
        else:
            break

if __name__ == "__main__":
    main()
