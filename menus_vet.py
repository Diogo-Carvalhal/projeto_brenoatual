from protocolo import enviar

def menu_vet(sock, user_id):
    while True:
        print("""
=== MENU VETERINÁRIO ===
1. Minhas Consultas
2. Atualizar Estado da Consulta
3. Registrar Diagnóstico
4. Consultar Histórico de Animal
0. Sair
""")
        op = input("Opção: ")

        if op == "1":
            print(enviar(sock, f"MINHAS_CONSULTAS {user_id}"))

        elif op == "2":
            cid = input("ID da Consulta: ")
            estado = input("Novo estado (agendada/em_atendimento/concluida): ")
            print(enviar(sock, f"ATUALIZAR_ESTADO {cid} {estado}"))

        elif op == "3":
            cc_tutor = input("Cartão de Cidadão do tutor: ").strip()

            # Listar animais
            resp = enviar(sock, f"LISTAR_ANIMAIS {cc_tutor}")
            print(resp)

            aid = input("Escolha o ID do Animal: ").strip()
            diag = input("Diagnóstico: ").strip()
            presc = input("Prescrição: ").strip()

            print(enviar(sock, f"REG_DIAGNOSTICO {cc_tutor} {diag} {presc}"))

            # VALOR DA CONSULTA
            valor = input("Insira o valor da consulta: ").strip()
            metodo = input("Método de pagamento (dinheiro/cartao): ").strip()

            print(enviar(sock, f"PAGAR_ULTIMA {aid} {valor} {metodo}"))

        elif op == "4":
            # Primeiro pede CC do tutor
            cc_tutor = input("Cartão de Cidadão do tutor: ").strip()
            # Chama o servidor para listar os animais desse CC
            resp = enviar(sock, f"LISTAR_ANIMAIS {cc_tutor}")
            print(f"Animais do tutor {cc_tutor}: {resp}")

            # Depois pede ID do animal para consultar histórico
            aid = input("Escolha o ID do Animal: ")
            print(enviar(sock, f"HISTORICO {cc_tutor}"))

        elif op == "0":
            break

        else:
            print("Opção inválida!")
