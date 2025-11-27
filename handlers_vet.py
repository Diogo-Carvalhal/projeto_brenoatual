def processar_vet(cmd, args, cursor, conn):
    if cmd == "MINHAS_CONSULTAS":
        # args = lista de vet_ids
        vet_ids = args
        todas_consultas = []

        for vet_id in vet_ids:
            cursor.execute("""
                SELECT c.id, a.id, a.nome, c.estado
                FROM consultas c
                JOIN animais a ON c.animal_id = a.id
                WHERE c.vet_id=%s AND c.estado != 'concluida'
            """, (vet_id,))
            consultas = cursor.fetchall()
            for c in consultas:
                todas_consultas.append({
                    "consulta_id": c[0],
                    "animal_id": c[1],
                    "animal_nome": c[2],
                    "estado": c[3]
                })

        if todas_consultas:
            return str(todas_consultas)
        else:
            return "NENHUMA_CONSULTA"

    elif cmd == "ATUALIZAR_ESTADO":
        # args = [consulta_id, novo_estado]
        consulta_id, estado = args

        cursor.execute("SELECT id FROM consultas WHERE id=%s", (consulta_id,))
        if cursor.fetchone() is None:
            return "CONSULTA_NAO_EXISTE"

        cursor.execute("UPDATE consultas SET estado=%s WHERE id=%s", (estado, consulta_id))
        conn.commit()
        return "ESTADO_ATUALIZADO"

    elif cmd == "REG_DIAGNOSTICO":
        # args = [cartao_cidadao, diagnostico, prescricao]
        cc_tutor, diagnostico, prescricao = args

        # Lista todos os animais do tutor
        cursor.execute("SELECT id, nome FROM animais WHERE tutor_cc=%s", (cc_tutor,))
        animais = cursor.fetchall()
        if not animais:
            return "TUTOR_NAO_EXISTE"

        # Mostra ao vet os animais do tutor
        lista_animais = {a[0]: a[1] for a in animais}
        print(f"[SERVIDOR] Animais do tutor {cc_tutor}: {lista_animais}")

        # Para simplificação, pega o primeiro animal ou pedir ID separadamente no cliente
        animal_id = animais[0][0]

        cursor.execute(
            "INSERT INTO historico(animal_id, diagnostico, prescricao) VALUES (%s,%s,%s)",
            (animal_id, diagnostico, prescricao)
        )
        conn.commit()
        return "DIAGNOSTICO_REGISTRADO"

    elif cmd == "HISTORICO":
        # args = lista de CCs
        cc_list = args
        historicos = {}

        for cc_tutor in cc_list:
            cursor.execute("SELECT id, nome FROM animais WHERE tutor_cc=%s", (cc_tutor,))
            animais = cursor.fetchall()
            if not animais:
                historicos[cc_tutor] = "TUTOR_NAO_EXISTE"
                continue

            # Lista todos os animais do tutor
            lista_animais = {a[0]: a[1] for a in animais}
            print(f"[SERVIDOR] Animais do tutor {cc_tutor}: {lista_animais}")

            registros_tutor = {}
            for animal in animais:
                animal_id, nome = animal
                cursor.execute("SELECT diagnostico, prescricao FROM historico WHERE animal_id=%s", (animal_id,))
                registros = cursor.fetchall()
                if registros:
                    registros_tutor[nome] = [{"diagnostico": r[0], "prescricao": r[1]} for r in registros]
                else:
                    registros_tutor[nome] = "HISTORICO_VAZIO"

            historicos[cc_tutor] = registros_tutor

        return str(historicos)

    return "COMANDO_DESCONHECIDO"
