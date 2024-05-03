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
    
    split_command = command.split()
    
    # Jika koneksi dengan server sudah terjalin
    if conn:
      # Mengirim pesan berupa perintah ke server
      client_socket.send(command.encode())
    

      # Jika pengguna memasukkan perintah upload yang didampingi dengan nama file
      if command.lower().startswith('upload') and len(split_command) > 1:
          # Menyimpan nama dokumen
          file_name = split_command[1]
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
      elif command.lower().startswith('download') and len(split_command) > 1:
          # Untuk menyimpan nama dokumen dan path dokumen
          file_name = ""
          filepath = ""
          
          # Jika ada argumen kedua
          if len(split_command) > 2:
              # Menyimpan argumen kedua
              second_arg = split_command[2]
              # Mendapatkan format dokumen
              origin_format = split_command[1].split('.')[-1]
              new_format = split_command[2].split('.')[-1]
              # Jika argumen kedua tidak mengandung slash dan backslah dan mengandung titik, langsung ambil sebagai nama dokumen
              if second_arg.find('\\') == -1 and second_arg.find('/') == -1 and second_arg.find('.') != -1:
                  # Menyimpan nama dokumen
                  file_name = second_arg
                  # Menyiapkan path dokumen
                  if origin_format == new_format:
                    filepath = os.path.join(FILE_DIR, file_name)
                  else:
                    print("Argumen tidak valid. Tidak dapat menggunggah dokumen manjadi format lain.")
                    continue
              # Jika argumen kedua mengandung slash atau tidak mengandung titik
              elif second_arg.find('/') > -1 or second_arg.find('.') == -1:
                  print("Argumen tidak valid. Perhatikan penulisan path!")
                  continue
              else:
                  # Mendapatkan nama file    
                  split_second_arg = second_arg.split("\\")
                  file_name = split_second_arg[len(split_second_arg)-1]   
                  # Menyiapkan path dokumen
                  filepath = os.path.join(FILE_DIR, second_arg)
          else:       
              file_name = split_command[1]
              # Menyiapkan path dokumen
              filepath = os.path.join(FILE_DIR, file_name)

          # Jika client mengunduh dokumen untuk disimpan di direktori tertentu
          if len(split_command) > 1:
              # Jika file ditemukan dalam direktori
              if os.path.isfile(filepath):
                  print(f"Dokumen dengan nama ({file_name}) sudah ada di direktori client.")  
                  continue
              else:              
                  file_data = client_socket.recv(BUFFER_SIZE) 
                  # Jika respon bukan '-1' atau dokumen tersedia dan siap diunduh
                  if file_data.decode() != '-1':
                    try:
                      # Membuat/menulis dokumen sesuai path
                      with open(filepath, 'wb') as f:
                          # Tulis respon server ke dokumen yang dibuat
                          f.write(file_data)
                      # Beri feedback
                      size = os.path.getsize(filepath) / (1024 * 1024)
                      print(f"Dokumen '{file_name}' ({size:.2f} MB) berhasil diunduh di direktori '{filepath}' client.")
                    except:
                      # Jika file tidak dapat dibuat karena direktori tidak ada atau kesalahan lain
                      print("Argumen tidak valid. Gagal mengunduh dokumen.")
                      continue

      # Menerima respon dari server, lalu menampilkannya
      if command.lower().startswith('download') == False:
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