import socket
from protocolo import enviar
from menus_admin import menu_admin
from menus_vet import menu_vet
from menus_cliente import menu_cliente

HOST = "127.0.0.1"
PORT = 5000

def main():
    sock = socket.socket()
    sock.connect((HOST, PORT))

    while True:
        print("\n=== BEM-VINDO À CLÍNICA VET ===")
        print("1. Login")
        print("2. Registrar novo UTILIZADOR")
        print("0. Sair")
        op = input("Opção: ").strip()

        if op == "0":
            break

        # ---------------------------
        # REGISTRO
        # ---------------------------
        x
        if op == "2":
            username = input("Escolha o username: ").strip()
            senha = input("Escolha a senha: ").strip()
            tipo = input("Tipo de utilizador (ADMIN/VET/CLIENTE): ").strip().upper()

            resp = enviar(sock, f"REGISTRO {username} {senha} {tipo}")

            if resp.strip() == "UTILIZADOR_REGISTRADO":
                    print("✔ Registro concluído! Agora faça login.")
            elif resp == "USUARIO_EXISTENTE":
                    print("⚠ Este username já existe.")
            elif resp == "TIPO_INVALIDO":
                    print("⚠ Tipo de utilizador inválido.")
            else:
                    print("⚠ Erro no registro.")

        # ---------------------------
        # LOGIN
        # ---------------------------
        elif op == "1":
            username = input("Username: ").strip()
            senha = input("Senha: ").strip()

            resp = enviar(sock, f"LOGIN {username} {senha}")

            if resp.startswith("LOGIN_OK"):
                partes = resp.split()
                tipo = partes[1]
                user_id = partes[2]

                print(f"✔ Login efetuado como {tipo}!")

                if tipo == "ADMIN":
                    menu_admin(sock, user_id)
                elif tipo == "VET":
                    menu_vet(sock, user_id)
                elif tipo == "CLIENTE":
                    menu_cliente(sock, user_id)

            else:
                print("❌ Login inválido.")

if __name__ == "__main__":
    main()
