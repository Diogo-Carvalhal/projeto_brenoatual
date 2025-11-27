def processar_admin(cmd, args, cursor, conn):
    if cmd == "ADD_VET":
        username, senha = args
        cursor.execute("INSERT INTO utilizadores(username, senha, tipo) VALUES(%s,%s,'VET')", (username, senha))
        conn.commit()
        return "VETERINARIO_ADICIONADO"

    elif cmd == "DEL_VET":
        vet_id = args[0]
        cursor.execute("DELETE FROM utilizadores WHERE id=%s AND tipo='VET'", (vet_id,))
        conn.commit()
        return "VETERINARIO_REMOVIDO"

    elif cmd == "LISTAR_CONSULTAS":
        cursor.execute("SELECT * FROM consultas")
        linhas = cursor.fetchall()
        return str(linhas)

    elif cmd == "RELATORIO":
        cursor.execute("SELECT COUNT(*) FROM consultas")
        total_consultas = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM animais")
        total_animais = cursor.fetchone()[0]
        return f"Total consultas: {total_consultas}, Total animais: {total_animais}"

    return "COMANDO_DESCONHECIDO"
