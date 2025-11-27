from protocolo import enviar

def menu_cliente(sock, user_id):
    while True:
        print("""
=== MENU CLIENTE ===
1. Registrar Animal
2. Agendar Consulta
3. Ver Minhas Consultas
4. Ver Histórico de Animal
5. Pagamento de Consulta
0. Sair
""")
        op = input("Opção: ").strip()

        # ---------------------------
        # Registrar Animal com CC
        # ---------------------------
        if op == "1":
            nome = input("Nome do animal: ").strip()
            especie = input("Espécie: ").strip()
            idade = input("Idade: ").strip()
            cc = input("Cartão de Cidadão do tutor: ").strip()
            resp = enviar(sock, f"REG_ANIMAL {nome} {especie} {idade} {cc}")
            if resp.strip() == "ANIMAL_REGISTRADO":
                print(f"✔ Animal '{nome}' registado com sucesso para o tutor {cc}.")
            else:
                print("⚠ Erro ao registar animal:", resp)

        # ---------------------------
        # Agendar Consulta
        # ---------------------------
        elif op == "2":
            print("\n=== Agendar Consulta ===")
            aid = input("ID do Animal: ").strip()
            ano = input("Ano (YYYY): ").strip()
            mes = input("Mês (MM): ").strip()
            dia = input("Dia (DD): ").strip()
            hora = input("Hora (HH, 24h): ").strip()
            minuto = input("Minuto (MM): ").strip()
            data_str = f"{ano}-{mes}-{dia} {hora}:{minuto}"
            vet = input("ID do Veterinário: ").strip()
            resp = enviar(sock, f"AGENDAR {aid} {data_str} {vet}")
            print(resp)

        # ---------------------------
        # Ver Minhas Consultas
        # ---------------------------
        elif op == "3":
            print("\n=== Ver Minhas Consultas ===")
            cc_tutor = input("Digite o seu Cartão de Cidadão: ").strip()
            resp = enviar(sock, f"VER_CONSULTAS {cc_tutor}")
            print(resp)

        # ---------------------------
        # Ver Histórico do Animal
        # ---------------------------
        elif op == "4":
            aid = input("ID do Animal: ").strip()
            resp = enviar(sock, f"VER_HISTORICO {aid}")
            print(resp)

        # ---------------------------
        # Pagamento de Consulta
        # ---------------------------
        elif op == "5":
            print("\n=== Pagamento de Consulta ===")
            cc_tutor = input("Digite o seu Cartão de Cidadão: ").strip()

            # Mostra apenas as consultas do tutor que ainda não foram pagas
            resp = enviar(sock, f"VER_CONSULTAS_PENDENTES {cc_tutor}")
            if resp.strip() == "NENHUMA_CONSULTA":
                print("❌ Não há consultas pendentes para pagamento.")
                continue

            print(f"Consultas disponíveis para pagamento:\n{resp}")

            consulta_id = input("Digite o ID da consulta que deseja pagar: ").strip()
            valor = input("Valor do pagamento: ").strip()
            metodo = input("Método (dinheiro/cartao): ").strip()

            # Envia comando de pagamento
            resp = enviar(sock, f"PAGAR {consulta_id} {valor} {metodo}")
            if resp.strip() == "PAGAMENTO_REGISTRADO":
                print("✔ Pagamento efetuado com sucesso!")
            else:
                print("❌ Erro ao registrar pagamento:", resp)


        # ---------------------------
        # Sair
        # ---------------------------
        elif op == "0":
            break

        else:
            print("Opção inválida!")
