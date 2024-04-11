import socket
import threading

clients = []  # To keep track of connected clients

def client_thread(conn, addr):
    print(f"Connected by {addr}")
    clients.append(conn)  # addds clients
    
    while True:
        try:
            message = conn.recv(1024).decode('utf-8')
            if message:
                print(f"Message from {addr}: {message}")
                # sends message to all othere clients
                for client in clients:
                    if client != conn:
                        client.sendall(f"Message from {addr}: {message}".encode('utf-8'))
            else:
                break
        except:
            print(f"Lost connection with {addr}")
            break
    
    conn.close()
    clients.remove(conn)  # removes clients

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen()
    print("Server is listening on localhost:12345")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=client_thread, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
