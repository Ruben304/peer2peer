import socket
import threading

# apply input sanitization
def sanitize(message):
    message = message.strip() # get rid of extra white spaces
    message = message.replace('\n', '').replace('\r', '') # get rid of character controls 
    maxLength = 400 # set a cap on message length size 
    if len(message) > maxLength: # use part of message that is within cap
        message = message[:maxLength]
    return message

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            print(f"\n{message}\nYour message: ", end="")
        except:
            print("You have been disconnected from the server.")
            sock.close()
            break

def main():
    host = 'localhost'
    port = 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host, port))
    
    threading.Thread(target=receive_messages, args=(server,), daemon=True).start()

    while True:
        message = input("Your message: ")
        message = sanitize(message)
        if message.lower() == 'exit':
            break
        server.send(message.encode('utf-8'))
    server.close()

if __name__ == "__main__":
    main()

