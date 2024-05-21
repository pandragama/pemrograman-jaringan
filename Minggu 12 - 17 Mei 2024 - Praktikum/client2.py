import socket
# Inisialisasi socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Menghubungkan ke server
server_address = ('localhost', 5000)
sock.connect(server_address)
while True:
  # Meminta input dari pengguna
  ekspresi = input('Masukkan ekspresi matamatika: ')
  # Mengirim pesan ke server
  sock.send(ekspresi.encode())
  # Keluar loop jika mengirimkan kode untuk keluar
  if ekspresi == '!q': break
  # Menerima pesan balasan dari server
  response = sock.recv(1024).decode()
  print('Hasil perhitungan:', response)
  
print('Koneksi diakhiri.')
# Menutup koneksi dengan server
sock.close()