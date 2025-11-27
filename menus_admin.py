from protocolo import enviar

def menu_admin(sock, user_id):
    while True:
        print("""
=== MENU ADMINISTRADOR ===
1. Adicionar Veterinário
2. Remover Veterinário
3. Listar Consultas
4. Relatórios da Clínica
0. Sair
""")
        op = input("Opção: ")

        if op == "1":
            u = input("Username do Vet: ")
            p = input("Senha: ")
            print(enviar(sock, f"ADD_VET {u} {p}"))

        elif op == "2":
            vid = input("ID do Vet: ")
            print(enviar(sock, f"DEL_VET {vid}"))

        elif op == "3":
            print(enviar(sock, "LISTAR_CONSULTAS"))

        elif op == "4":
            print(enviar(sock, "RELATORIO"))

        elif op == "0":
            break

        else:
            print("Opção inválida!")
