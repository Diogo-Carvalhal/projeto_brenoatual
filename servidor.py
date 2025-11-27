import socket
from bd import conectar
from protocolo import parse_comando
from handlers_admin import processar_admin
from handlers_vet import processar_vet
from handlers_cliente import processar_cliente

HOST = "127.0.0.1"
PORT = 5000

def autenticar(cursor, username, senha):
    cursor.execute("SELECT id, tipo FROM utilizadores WHERE username=%s AND senha=%s", (username, senha))
    r = cursor.fetchone()
    if r:
        return r[0], r[1]
    return None, None

def registar_animal(args, cursor, conn):
    """
    Regista um animal associado a um tutor pelo Cartão de Cidadão (CC).
    args = [nome, especie, idade, tutor_cc]
    """
    if len(args) != 4:
        return "ERRO_PARAMETROS"

    nome, especie, idade, tutor_cc = args

    # Regista o animal diretamente na tabela animais
    cursor.execute(
        "INSERT INTO animais(nome, especie, idade, tutor_cc) VALUES (%s, %s, %s, %s)",
        (nome, especie, idade, tutor_cc)
    )
    conn.commit()

    print(f"[SERVIDOR] Novo animal registado: {nome}, espécie={especie}, tutor_cc={tutor_cc}")

    return "ANIMAL_REGISTRADO"


def processar_completo(msg, user_id, user_tipo, cursor, conn):
    cmd, args = parse_comando(msg)
    if cmd is None:
        return "ERRO"

    if cmd.upper() == "REG_ANIMAL":
        return registar_animal(args, cursor, conn)

    if user_tipo == "ADMIN":
        return processar_admin(cmd, args, cursor, conn)
    elif user_tipo == "VET":
        return processar_vet(cmd, args, cursor, conn)
    elif user_tipo == "CLIENTE":
        return processar_cliente(cmd, args, cursor, conn)

    return "PERMISSAO_NEGADA"

def processar_cliente(cmd, args, cursor, conn):
    if cmd == "PAGAR":
        # args = [consulta_id, valor, metodo]
        if len(args) != 3:
            return "ERRO_PARAMETROS"

        consulta_id, valor, metodo = args

        # Verifica se a consulta existe
        cursor.execute("SELECT id FROM consultas WHERE id=%s", (consulta_id,))
        if cursor.fetchone() is None:
            return "CONSULTA_NAO_EXISTE"

        # Regista o pagamento
        cursor.execute(
            "INSERT INTO pagamentos(consulta_id, valor, metodo) VALUES(%s,%s,%s)",
            (consulta_id, valor, metodo)
        )
        conn.commit()
        return "PAGAMENTO_REGISTRADO"

    elif cmd == "VER_PAGAMENTOS":
        # args = [cartao_cidadao]
        cc_tutor = args[0]
        cursor.execute("""
            SELECT p.id, p.consulta_id, p.valor, p.metodo, c.data
            FROM pagamentos p
            JOIN consultas c ON p.consulta_id = c.id
            JOIN animais a ON c.animal_id = a.id
            WHERE a.tutor_cc = %s
            ORDER BY c.data
        """, (cc_tutor,))
        pagamentos = cursor.fetchall()
        if pagamentos:
            return str(pagamentos)
        else:
            return "NENHUM_PAGAMENTO"

    return "COMANDO_DESCONHECIDO"

def main():
    con = conectar()
    cur = con.cursor()
    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen(5)
    print("Servidor ligado...")

    while True:
        c, addr = s.accept()
        print("Cliente conectado:", addr)
        user_id = None
        user_tipo = None

        while True:
            dados = c.recv(4096).decode()
            if not dados:
                break

            partes = dados.strip().split()

            # ------------------------------------------------
            #  REGISTRO: REGISTRO username senha tipo
            # ------------------------------------------------
            if len(partes) >= 1 and partes[0].upper() == "REGISTRO":
                if len(partes) != 4:
                    resposta = "ERRO_REGISTRO"
                else:
                    username, senha, tipo = partes[1], partes[2], partes[3].upper()
                    
                    if tipo not in ["ADMIN", "VET", "CLIENTE"]:
                        resposta = "TIPO_INVALIDO"
                    else:
                        cur.execute("SELECT id FROM utilizadores WHERE username=%s", (username,))
                        if cur.fetchone():
                            resposta = "USUARIO_EXISTENTE"
                        else:
                            cur.execute(
                                "INSERT INTO utilizadores(username, senha, tipo) VALUES(%s,%s,%s)",
                                (username, senha, tipo)
                            )
                            con.commit()

                            # Mostrado apenas no servidor
                            print(f"[SERVIDOR] Novo utilizador registado: username={username}, tipo={tipo}")

                            # Enviado ao cliente
                            resposta = "UTILIZADOR_REGISTRADO"

            # ------------------------------------------------
            #  LOGIN: LOGIN username senha
            # ------------------------------------------------
            elif len(partes) >= 3 and partes[0].upper() == "LOGIN":
                username, senha = partes[1], partes[2]
                user_id, user_tipo = autenticar(cur, username, senha)

                if user_id:
                    resposta = f"LOGIN_OK {user_tipo} {user_id}"
                else:
                    resposta = "LOGIN_INVALIDO"

            else:
                if user_id is None:
                    resposta = "PERMISSAO_NEGADA"
                else:
                    resposta = processar_completo(dados, user_id, user_tipo, cur, con)

            c.sendall((resposta + "\n").encode())

        c.close()

if __name__ == "__main__":
    main()
