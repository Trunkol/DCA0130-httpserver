# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: PROF. CARLOS M D VIEGAS (viegas 'at' dca.ufrn.br)
#
# SCRIPT: Base de um servidor HTTP (python 3)
#

# importacao das bibliotecas
import socket

# definicao do host e da porta do servidor
HOST = '' # ip do servidor (em branco)
PORT = 8080 # porta do servidor

# cria o socket com IPv4 (AF_INET) usando TCP (SOCK_STREAM)
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# permite que seja possivel reusar o endereco e porta do servidor caso seja encerrado incorretamente
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# vincula o socket com a porta (faz o "bind" do IP do servidor com a porta)
listen_socket.bind((HOST, PORT))

# "escuta" pedidos na porta do socket do servidor
listen_socket.listen(1)

# imprime que o servidor esta pronto para receber conexoes
print ('Serving HTTP on port %s ...' % PORT)

while True:
    # aguarda por novas conexoes
    client_connection, client_address = listen_socket.accept()
    # o metodo .recv recebe os dados enviados por um cliente atraves do socket
    request = client_connection.recv(1024)
    # imprime na tela o que o cliente enviou ao servidor
    print (request.decode('utf-8'))
    # declaracao da resposta do servidor

    dict_request = str(request).split(' ')
    http_response = """\
HTTP/1.1 200 OK

Hello, World!
"""
    print(request)
    if dict_request[0] == 'GET':
        try:
            header = 'HTTP/1.1 200 OK\n\n'
            if dict_request[1] in ('/', 'index.html'):
                conteudo = open('index.html', 'r').read()
            else:
                arquivo = dict_request[1].strip('/')
                conteudo = open(arquivo, 'r').read()
        except IOError as e:
            header = 'HTTP/1.1 404 Not Found\n\n'
            conteudo = open('not_found.html', 'r').read()
    else:
        header = 'HTTP/1.1 400 Bad Request\n\n'
        conteudo = open('bad_request.html', 'r').read()

    http_response = header + conteudo

    # servidor retorna o que foi solicitado pelo cliente (neste caso a resposta e generica)
    client_connection.send(http_response.encode('utf-8'))
    # encerra a conexao
    client_connection.close()

# encerra o socket do servidor
listen_socket.close()