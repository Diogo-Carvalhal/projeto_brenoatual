class Utilizador:
    def __init__(self, id, username, tipo):
        self.id = id
        self.username = username
        self.tipo = tipo

class Administrador(Utilizador):
    pass

class Veterinario(Utilizador):
    pass

class Cliente(Utilizador):
    pass
