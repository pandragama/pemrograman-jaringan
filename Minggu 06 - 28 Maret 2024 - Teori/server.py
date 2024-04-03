# Modul socket, menyediakan fungsi dan metode untuk membuat koneksi jaringan
import socket
# Modul os, menyediakan fungsi dan metode untuk berinteraksi dengan sistem operasi
import os

# ALamat IP dan Port Server
SERVER_HOST = 'localhost'
SERVER_PORT = 12345
# Ukuran buffer untuk menerima pesan/data (1 Mb)
BUFFER_SIZE = 1048600  
# Direktori dokumen server
FILE_DIR = 'server_files'

# Memastikan keberadaan direktori server_files
if not os.path.exists(FILE_DIR):
    os.makedirs(FILE_DIR)

# Fungsi untuk mengurus perintah dari client
def handle_client(client_socket):
    while True:
        # Menerima perintah client
        command = client_socket.recv(BUFFER_SIZE).decode()
        # Menyimpan perintah yang sudah dipecah
        split_command = command.split()
        # Menyimpan perintah Client
        action = split_command[0].lower()
        print(f"Menerima perintah: {command}")
        
        # Mengurus perintah ls atau list
        if action == 'ls':
            # Mendapatkan daftar dokumen dalam direktori
            files = os.listdir(FILE_DIR)
            # Jika direktori tidak kosong
            if len(files) > 0:
                # Menformat daftar dokumen menjadi daftar yang dipisahkan baris baru (String)
                files_list = '\n'.join(files)
                # Mengirimkan daftar dokumen yang sudah disiapkan
                client_socket.sendall(files_list.encode())
            else:
                client_socket.sendall(f"Direktori '{FILE_DIR}' kosong.".encode())

        # Mengurus perintah rm atau remove dan parameternya (nama dokumen)
        elif action == 'rm' and len(split_command) > 1:
            # Menyimpan nama dokumen
            file_name = split_command[1]
            # Menyiapkan path dokumen
            filepath = os.path.join(FILE_DIR, file_name)
            try:
                # Coba hapus dokumen sesuai path, lalu beritahu client
                os.remove(filepath)
                client_socket.send(f"Dokumen '{file_name}' berhasil dihapus".encode())
            except FileNotFoundError:
                # Jika dokumen tidak ditemukan sesuai path, maka peringatkan client
                client_socket.send(f"Dokumen '{file_name}' tidak ditemukan".encode())

        # Mengurus perintah upload dan parameternya (nama dokumen)
        elif action == 'upload' and len(split_command) > 1:
            # Menerima data dari client
            file_data = client_socket.recv(BUFFER_SIZE)
            # Jika data yang diterima bukan '-1' atau dokumen tersedia dan siap diupload
            if file_data.decode() != '-1':
                # Menyimpan nama dokumen
                file_name = split_command[1]
                # Menyiapkan path dokumen
                filepath = os.path.join(FILE_DIR, file_name)
                # Membuat/menulis dokumen sesuai path
                with open(filepath, 'wb') as f:
                    # Menerima data file yang "diupload" client, lalu menuliskannya ke dokumen yang dibuat
                    f.write(file_data)
                # Memberi tahu client
                client_socket.send(f"Dokumen '{file_name}' berhasil diunggah".encode())                
        
        # Mengurus perintah download dan parameternya (nama dokumen)
        elif action == 'download' and len(split_command) > 1:
            # Menyimpan nama dokumen
            file_name = split_command[1]
            # Menyiapkan path dokumen
            filepath = os.path.join(FILE_DIR, file_name)
            # Jika path merujuk pada sebuah dokumen, 
            if os.path.isfile(filepath):
                # maka baca data dokumen tersebut dan kirim datanya ke client
                with open(filepath, 'rb') as f:
                    client_socket.sendall(f.read())
                client_socket.send(f"Dokumen '{file_name}' berhasil diunduh".encode())
            else:
                # Awali dengan mengirim kode peringatan bahwa dokumen tidak ditemukan
                client_socket.send('-1'.encode())
                # Lalu beri pesan peringatannya
                client_socket.send(f"Dokumen '{file_name}' tidak ditemukan".encode())
    
        # Mengurus perintah size dana parameternya (nama dokumen)
        elif action == 'size' and len(split_command) > 1:
            # Menyimpan nama dokumen
            file_name = split_command[1]
            # Menyiapkan path dokumen
            filepath = os.path.join(FILE_DIR, file_name)
            # Jika path merujuk pada sebuah dokumen, maka hitung ukuran file dalam satuan MegaByte
            if os.path.isfile(filepath):
                size = os.path.getsize(filepath) / (1024 * 1024)
                client_socket.send(f"Ukuran dokumen '{file_name}': {size:.2f} MB".encode())
            else:
                client_socket.send(f"Dokumen '{file_name}' tidak ditemukan".encode())

        # Mengurus perintah byebye
        elif action == 'byebye':
            # Tutup koneksi client socket
            client_socket.close()
            print("Koneksi dengan client diakhiri")
            return
        
        # Mengurus perintahh connme
        elif action == 'connme':
            client_socket.send(b'Sedang terhubung dengan server')
        
        # Mengurus perintah yang tidak disediakan
        else:
            # Mengirim pemberitahuan ke client
            client_socket.send('Perintah tidak valid'.encode())

# Menyiapkan server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print(f"Server siap menerima koneksi di {SERVER_HOST}:{SERVER_PORT}")

# Menerima clients
while True:
    client_conn, client_addr = server_socket.accept()
    print(f"Menerima koneksi dari {client_addr}")
    handle_client(client_conn)