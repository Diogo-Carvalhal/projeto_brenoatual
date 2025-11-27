import mysql.connector

def criar_bd():
    # Conexão inicial sem database
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cur = con.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS clinica;")
    con.commit()
    con.close()

    # Conexão com a database clinica
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="clinica"
    )
    cur = con.cursor()

    # ---------------------------
    # TABELA UTILIZADORES
    # ---------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS utilizadores(
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50),
        senha VARCHAR(50),
        tipo ENUM('ADMIN','VET','CLIENTE')
    );
    """)

    # ---------------------------
    # TABELA ANIMAIS (com tutor_cc)
    # ---------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS animais(
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(50),
        especie VARCHAR(50),
        idade INT,
        tutor_cc VARCHAR(20) NOT NULL
    );
    """)

    # ---------------------------
    # TABELA CONSULTAS (com data)
    # ---------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS consultas(
        id INT AUTO_INCREMENT PRIMARY KEY,
        animal_id INT,
        vet_id INT,
        data DATETIME NOT NULL,
        estado ENUM('agendada','em_atendimento','concluida'),
        FOREIGN KEY (animal_id) REFERENCES animais(id),
        FOREIGN KEY (vet_id) REFERENCES utilizadores(id)
    );
    """)

    # ---------------------------
    # TABELA HISTÓRICO
    # ---------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS historico(
        id INT AUTO_INCREMENT PRIMARY KEY,
        animal_id INT,
        diagnostico TEXT,
        prescricao TEXT,
        data DATETIME DEFAULT NOW(),
        FOREIGN KEY (animal_id) REFERENCES animais(id)
    );
    """)

    # ---------------------------
    # TABELA PAGAMENTOS
    # ---------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pagamentos(
        id INT AUTO_INCREMENT PRIMARY KEY,
        consulta_id INT,
        valor DECIMAL(10,2),
        metodo ENUM('dinheiro','cartao'),
        FOREIGN KEY (consulta_id) REFERENCES consultas(id)
    );
    """)

    con.commit()
    con.close()


if __name__ == "__main__":
    criar_bd()
    print("BD criada/verificada.")
