# === server/server.py ===
import socket
import threading
import pickle

# Player starting positions
positions = [(100, 100), (700, 100), (100, 500), (700, 500)]
players = {}  # {id: (x, y)}

HOST = '0.0.0.0'
PORT = 10001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(4)

print("[SERVER] Waiting for players...")

def client_thread(conn, player_id):
    global players

    # Send initial position
    conn.send(pickle.dumps((player_id, positions[player_id])))
    while True:
        try:
            data = pickle.loads(conn.recv(1024))
            if not data:
                break
            players[player_id] = data  # Update player position

            # Send all players' data back
            conn.sendall(pickle.dumps(players))
        except:
            break

    print(f"[DISCONNECT] Player {player_id} left.")
    conn.close()
    del players[player_id]

player_id_counter = 0
while player_id_counter < 4:
    conn, addr = server.accept()
    print(f"[CONNECTED] Player {player_id_counter} from {addr}")
    threading.Thread(target=client_thread, args=(conn, player_id_counter)).start()
    player_id_counter += 1
