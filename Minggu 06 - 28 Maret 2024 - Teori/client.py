# Modul socket, menyediakan fungsi dan metode untuk membuat koneksi jaringan
import socket
# Modul os, menyediakan fungsi dan metode untuk berinteraksi dengan sistem operasi
import os

# ALamat IP dan Port Server
SERVER_HOST = 'localhost'
SERVER_PORT = 12345
# Ukuran buffer untuk menerima pesan/data (1 Mb)
BUFFER_SIZE = 1048600  
# Direktori dokumen client
FILE_DIR = 'client_files'

# Memastikan keberadaan direktori client_files
if not os.path.exists(FILE_DIR):
    os.makedirs(FILE_DIR)

# Variabel untuk menyimpan socket dan status koneksi
client_socket = None
conn = False

# Client operations
while True:
    # Menerima input pengguna
    command = input(f"Masukkan perintah [{'Client-Server'if conn else'Client'}] > ")
    
    # Jika koneksi dengan server sudah terjalin
    if conn:
      # Mengirim pesan berupa perintah ke server
      client_socket.send(command.encode())

      # Jika pengguna memasukkan perintah upload yang didampingi dengan nama file
      if command.lower().startswith('upload') and len(command.split()) > 1:
          # Menyimpan nama dokumen
          file_name = command.split()[1]
          # Menyiapkan path dokumen
          filepath = os.path.join(FILE_DIR, file_name)
          if os.path.isfile(filepath):
              with open(filepath, 'rb') as f:
                  client_socket.sendall(f.read())
          else:
              # Kirim kode peringatan bahwa dokume tidak tersedia untuk diupload
              client_socket.send('-1'.encode())
              print(f"Dokumen '{filepath}' tidak ditemukan")  
              continue        

      # Jika pengguna memasukkan perintah download yang didampingi dengan nama file
      elif command.lower().startswith('download') and len(command.split()) > 1:
          # Menerima respon server
          file_data = client_socket.recv(BUFFER_SIZE)
          # Jika respon bukan '-1' atau dokumen tersedia dan siap diunduh
          if file_data.decode() != '-1':
            # Menyimpan nama dokumen
            file_name = command.split()[1]
            # Menyiapkan path dokumen
            filepath = os.path.join(FILE_DIR, file_name)
            # Membuat/menulis dokumen sesuai path
            with open(filepath, 'wb') as f:
                # Tulis respon server ke dokumen yang dibuat
                f.write(file_data)
      
      # Menerima respon dari server, lalu menampilkannya
      response = client_socket.recv(BUFFER_SIZE)
      print(response.decode())

      # Mengurus perintah byebye
      if command.lower() == 'byebye':
          client_socket.close()
          conn = False
          print("Koneksi dengan server diakhiri")
      
    else:
      # Mengurus perintah connme
      if command.lower() == 'connme':
        # Membuat socket dan menghubungkannya ke alamat dan port server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Socket (Client-Server) terhubung.")
        # Status koneksi menjadi true
        conn = True
      else:
        # Kondisi default, mengingatkan pengguna untuk menghubungkan client dengan server
        print("Socket (Client-Server) tidak terhubung. Tidak dapat mengirim atau menerima data.")
        print("Jalankan perintah 'connme' untuk menghubungkan dengan server socket.")