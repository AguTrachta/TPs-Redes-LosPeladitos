import socket

HOST = '0.0.0.0'  # Escuchar en todas las interfaces
PORT = 8080       # Puerto TCP a usar

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor esperando conexión en {HOST}:{PORT}...")
        conn, addr = s.accept()
        with conn:
            print(f"Conectado con {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Recibido: {data.decode()}")

if __name__ == "__main__":
    main()