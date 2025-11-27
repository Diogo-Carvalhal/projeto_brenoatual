def processar_cliente(cmd, args, cursor, conn):

    # ----------------------------------------
    # ADICIONAR ANIMAL
    # ----------------------------------------
    if cmd == "ADD_ANIMAL":
        nome, especie, idade, tutor_id = args
        cursor.execute("INSERT INTO animais(nome, especie, idade, tutor_id) VALUES(%s,%s,%s,%s)",
                       (nome, especie, idade, tutor_id))
        conn.commit()
        return "ANIMAL_ADICIONADO"


    # ----------------------------------------
    # LISTAR ANIMAIS PELO CC DO TUTOR
    # ----------------------------------------
    elif cmd == "LISTAR_ANIMAIS":
        cc_tutor = args[0]
        cursor.execute("SELECT id, nome, especie FROM animais WHERE tutor_cc=%s", (cc_tutor,))
        animais = cursor.fetchall()

        if animais:
            return "\n".join([f"ID: {a[0]} | Nome: {a[1]} | Espécie: {a[2]}" for a in animais])
        else:
            return "SEM_ANIMAIS"


    # ----------------------------------------
    # REGISTAR DIAGNÓSTICO
    # ----------------------------------------
    elif cmd == "REG_DIAGNOSTICO":
        cc_tutor, diag, presc = args

        # Descobrir o animal mais recente do cliente
        cursor.execute("""
            SELECT c.id 
            FROM consultas c
            JOIN animais a ON c.animal_id = a.id
            WHERE a.tutor_cc = %s
            ORDER BY c.data DESC
            LIMIT 1
        """, (cc_tutor,))
        consulta = cursor.fetchone()

        if not consulta:
            return "SEM_CONSULTAS"

        consulta_id = consulta[0]

        cursor.execute(
            "INSERT INTO historico(consulta_id, diagnostico, prescricao) VALUES(%s,%s,%s)",
            (consulta_id, diag, presc)
        )
        conn.commit()
        return "DIAGNOSTICO_REGISTADO"


    # ----------------------------------------
    # PAGAR A ÚLTIMA CONSULTA DO ANIMAL
    # ----------------------------------------
    elif cmd == "PAGAR_ULTIMA":
        animal_id, valor, metodo = args

        # Obter a última consulta do animal
        cursor.execute("""
            SELECT id FROM consultas 
            WHERE animal_id=%s 
            ORDER BY data DESC LIMIT 1
        """, (animal_id,))
        consulta = cursor.fetchone()

        if not consulta:
            return "SEM_CONSULTAS"

        consulta_id = consulta[0]

        # Verificar se já foi paga
        cursor.execute("SELECT id FROM pagamentos WHERE consulta_id=%s", (consulta_id,))
        if cursor.fetchone():
            return "CONSULTA_JA_PAGA"

        # Registrar pagamento
        cursor.execute("""
            INSERT INTO pagamentos (consulta_id, valor, metodo)
            VALUES (%s, %s, %s)
        """, (consulta_id, valor, metodo))
        conn.commit()

        return "PAGAMENTO_REGISTADO"


    # ----------------------------------------
    # VER CONSULTAS POR CC
    # ----------------------------------------
    elif cmd == "VER_CONSULTAS":
        tutor_cc = args[0]

        cursor.execute("""
            SELECT c.id, a.nome AS animal, c.vet_id, c.data, c.estado
            FROM consultas c
            JOIN animais a ON c.animal_id = a.id
            WHERE a.tutor_cc = %s
            ORDER BY c.data
        """, (tutor_cc,))

        consultas = cursor.fetchall()
        if consultas:
            return "\n".join([
                f"ID: {c[0]}, Animal: {c[1]}, Vet: {c[2]}, Data: {c[3]}, Estado: {c[4]}"
                for c in consultas
            ])
        return "NENHUMA_CONSULTA"


    # ----------------------------------------
    # VER HISTÓRICO
    # ----------------------------------------
    elif cmd == "VER_HISTORICO":
        animal_id = args[0]
        cursor.execute("SELECT * FROM historico WHERE animal_id=%s", (animal_id,))
        return str(cursor.fetchall())


    # ----------------------------------------
    # COMANDO DESCONHECIDO
    # ----------------------------------------
    return "COMANDO_DESCONHECIDO"
