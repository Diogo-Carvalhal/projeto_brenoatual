def enviar(sock, msg):
    """
    Envia mensagem para o servidor e retorna a resposta.
    """
    sock.sendall((msg + "\n").encode())
    resp = sock.recv(4096).decode().strip()
    return resp
