import socket

s = socket.socket()
host = socket.gethostname()
port = 8080
s.connect((host, port))

print("Menyambungkan ke Server")

message = s.recv(1024)
message = message.decode()
print("Pesan dari server : ", message)

while 1:
    message = s.recv(1024)
    message = message.decode()
    print("Server : ", message)
    message = s.recv(1024)
    message = message.decode()
    print("Client_1 : ", message)
    message = s.recv(1024)
    message = message.decode()
    print("Client_2 : ", message)
    message = s.recv(1024)
    message = message.decode()
    print("Client_3 : ", message)
    new_message = input("Masukkan Pesan : ")
    new_message = str(new_message).encode()
    s.send(new_message)
    print("Pesan Terkirim")
