import socket
import threading
import random
import time

# Membuat socket UDP untuk client dan menyambungkannya ke port random
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("localhost", random.randint(8000, 9000)))

# List untuk menyimpan variabel pendukung permainan
status = [False]
answerSession = [False]
deadline = [False]
counter = [0]

# Awali dengan masukkan username agar alamat bisa disimpan server
name = input("Username: ")

# Fungsi untuk menghandle permainan
def game():
  # Looping selama selama permainan belumm selesai
  while not status[0]:
    try:
      message, _ = client.recvfrom(1024)
      
      # Salam dari server
      if message.decode().startswith("GREETING_TAG:"):
        str = message.decode()[message.decode().index(":")+1:]
        print(str)
        
      # Client menyerah/keluar
      elif message.decode().startswith("SURREND_TAG:"):
        str = message.decode()[message.decode().index(":")+1:]
        print(str)
        # Permainan selesai = TRUE
        status[0] = True
      
      # Client menyerah/keluar
      elif message.decode().startswith("FAILED_TAG:"):
        str = message.decode()[message.decode().index(":")+1:]
        print(str)
        # Permainan selesai = TRUE
        status[0] = True
      
      # Pertanyaan dari server
      elif message.decode().startswith("QUESTION_TAG:"):
        str = message.decode()[message.decode().index(":")+1:]
        print(str)
        
        # Sesi menjawab 5 detik
        answerSession[0] = True
        answer = input("")
        answerSession[0] = False
        counter[0] = 0
        
        # Jika belum 5 detik, maka kirim jawaban
        if deadline[0] == False:
          client.sendto(f"ANSWER_TAG:{answer}".encode(), ("localhost", 9999))
        # Jika deadline, kirim tag deadline
        else:
          client.sendto("DEADLINE_TAG".encode(), ("localhost", 9999))
        
    except:
      pass

# Buat dan jalankan thread daemon untuk menjalankan fungsi game di balik layar
t = threading.Thread(target=game, daemon=True)
t.start()

# mengirim username dengan tag signup
client.sendto(f"SIGNUP_TAG:{name}".encode(), ("localhost", 9999))

# Looping di thread utama
while True:
  # Jika permainan selesai adalah true, maka tutup koneksi dan akhiri program
  if status[0] == True:
    client.close()
    exit()
  
  # Jika sedang dalam sesi menjawab, hitung sesi selama 5 detik
  if answerSession[0] == True:
    time.sleep(1)
    counter[0] += 1
    # Jika sudah lebih dari 5 detik, maka deadline bernilai true
    if counter[0] >= 5:
      deadline[0] = True