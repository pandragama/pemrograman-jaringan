import socket
import threading
import queue
import random
import time

# Menyiapkan list dan struktur data queue
messages = queue.Queue()  # Menyimpan pesan masuk sementara
clients = []              # Menyimpan data client

# Membuat socket UDP untuk client
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 9999))

# Fungsi untuk mendapatkan warna dalam inggris dan indonesia
def randColor():
  # 20 warna (question, answer)
  palette = [
    ("red", "merah"),
    ("blue", "biru"),
    ("green", "hijau"),
    ("yellow", "kuning"),
    ("black", "hitam"),
    ("white", "putih"),
    ("purple", "ungu"),
    ("orange", "oranye"),
    ("grey", "abu-abu"),
    ("pink", "merah muda"),
    ("brown", "coklat"),
    ("cyan", "biru muda"),
    ("magenta", "magenta"),
    ("lime", "hijau muda"),
    ("maroon", "merah tua"),
    ("navy", "biru tua"),
    ("olive", "zaitun"),
    ("teal", "biru hijau"),
    ("violet", "violet"),
    ("indigo", "nila"),
  ]
  while True:
    question, answer = random.choice(palette)
    # Jika warna tidak dimiliki client manapun dalam clients, maka kembalikan warna tersebut
    if not any(client[1] == question for client in clients):
      return (question, answer)

# Fungsi untuk menyiapkan pertanyaan dan mengirimnya ke client
def generateQuestion(clientData):
  # isi clientData = [addr, question, answer, score]
  question, answer = randColor()
  clientData[1] = question
  clientData[2] = answer
  # Mengirim pertanyaan ke client setelah 5 detik
  time.sleep(5)
  server.sendto(f"QUESTION_TAG:\nPoin Tersimpan: {clientData[3]}\nPertanyaan: Terjemahan dari kata \"{question}\" adalah..\nJawab: ".encode(), clientData[0])

# Fungsi untuk memeriksa jawaban client
def checkAnswer(clientData, answer):
  if clientData[2] == answer:
    clientData[3] += 100
    server.sendto(f"GREETING_TAG:\nBENAR. Poin +100!\nBABAK BERIKUTNYA AKAN DIMULAI DALAM 5 DETIK..".encode(), clientData[0])
    generateQuestion(clientData)
  else:
    server.sendto(f"FAILED_TAG:\nSALAH. Kamu sudah berjuang, pantang menyerah kawan!\nPoin Akhir: {clientData[3]}\nTerimakasih sudah bermain! Semangat!\n".encode(), clientData[0])
    
# Fungsi untuk menerima pesan para client
def receive():
  while True:
    try:
      message, addr = server.recvfrom(1024)
      messages.put((message, addr))
    except:
      pass

# Fungsi untuk mengurus pesan-pesan yang masuk
def handle():
  while True:
    # Selama queue messages belum kosong
    while not messages.empty():
      message, addr = messages.get()
      print(message.decode())
      
      # Jika alamat yang diterima belum ada di client manapun dalam list clients
      if not any(client[0] == addr for client in clients):
        # Tambahkan data client meliputi
        # (address, question, answer, score)
        clients.append([addr, "", "", 0])
      
      # Iterasi setiap client
      for client in clients:
        try:
          # Jika pesan yang masuk dari client pada iterasi ini
          if client[0] == addr:
            
            # Client Masuk
            if message.decode().startswith("SIGNUP_TAG:"):
              name = message.decode()[message.decode().index(":")+1:]
              server.sendto(f"GREETING_TAG:\nSelamat bergabung {name}!\n=== ATURAN MAIN ===\n> Terjamahkan nama warna dalam 5 detik.\n> 5 detik setelahnya akan masuk babak berikutnya.\n> Setiap babak berhadiah 100 poin.\n> Kirim \"!q\" untuk menyerah atau keluar permainan.\n> Babak akan terus berjalan sampai kalah, terlambat, atau menyerah.\nPERMAINAN AKAN DIMULAI DALAM 5 DETIK..\n".encode(), client[0])
              generateQuestion(client)
            
            # Client Jawab
            elif message.decode().startswith("ANSWER_TAG:"):
              str = message.decode()[message.decode().index(":")+1:]
              # Jika client menyerah
              if str == "!q":
                server.sendto(f"SURREND_TAG:\nTerima kasih telah bergabung!\n".encode(), client[0])
              else:
                # Memeriksa jawaban biasa
                checkAnswer(client, str)
            # Client terlewat deadline
            elif message.decode() == "DEADLINE_TAG":
                server.sendto(f"FAILED_TAG:\nTERLAMBAT. Batas waktu menjawab (5 detik) sudah terlewat. Lain kali, waspadai waktunya kawan!\nPoin Akhir: {client[3]}\nTerimakasih sudah bermain! Semangat!\n".encode(), client[0])
            
            # Untuk Kemungkinan lain apabila terjadi kesalahan tag (untuk debugging)              
            # else:
            #   server.sendto(message, client[0])
              
        except:
          client.remove(message)

# Buat thread untuk menjalankan receive dan handle
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=handle)

# Jalankan thread yang sudah dibuat
t1.start()
t2.start()
      