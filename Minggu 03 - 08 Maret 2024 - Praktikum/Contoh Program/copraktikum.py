# Mengimpor modul socket
import socket

# Menginisialisasi socket untuk suatu entitas
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server_address = ('localhost', 8000)

server_socket.bind(('localhost', 8000))

server_socket.listen(5)

print("Waiting for connection...")
client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address}")

import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)


import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Mengatur opsi SO_LINGER
linger_option = socket.LingerOption(True, 30)  # True: menunggu, 30: waktu penundaan dalam detik
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, linger_option)
