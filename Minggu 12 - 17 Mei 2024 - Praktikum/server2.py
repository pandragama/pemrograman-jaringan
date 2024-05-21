import socket
# Inisialisasi socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind socket ke alamat dan port tertentu
server_address = ('localhost', 5000)
sock.bind(server_address)
# Menunggu koneksi masuk
sock.listen(1)
print('Menunggu koneksi dari klien...')
# Menerima koneksi dari klien
client_socket, client_address = sock.accept()
print('Terhubung dengan klien:', client_address)

while True:
  # Menerima pesan dari klien
  data = client_socket.recv(1024).decode()
  print('Pesan diterima dari klien:', data)
  # Keluar loop jika menerima kode untuk keluar
  if data == '!q': break
  # Memisahkan operator dan operand
  ekspresi = data.split()
  # Melakukan perhitungan matematika
  temp = 0
  for index, item in enumerate(ekspresi):
    if index == 0:
      temp += int(item)
    elif index % 2 != 0:
      if item == '+':
        temp += int(ekspresi[index+1])
      elif item == '-':
        temp -= int(ekspresi[index+1])
      elif item == '*':
        temp *= int(ekspresi[index+1])
      elif item == '/':
        temp /= int(ekspresi[index+1])
  
  # Mengirim pesan balasan berisi hasil perhitungan ke klien
  response = str(temp)
  client_socket.send(response.encode())

# Menutup koneksi dengan klien
client_socket.close()