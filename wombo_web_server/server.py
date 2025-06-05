import socket
import os

HOST, PORT = '127.0.0.1', 8080
BASE_DIR = './www'

MIME_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.js': 'application/javascript'
}

def get_mime_type(file_path):
    ext = os.path.splitext(file_path)[1]
    return MIME_TYPES.get(ext, 'application/octet-stream')

def handle_request(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    lines = request.splitlines()
    if not lines:
        return

    requested_file = lines[0].split(' ')[1]
    if requested_file == '/':
        requested_file = '/index.html'

    file_path = os.path.join(BASE_DIR, requested_file.lstrip('/'))

    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        content_type = get_mime_type(file_path)
        response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n".encode('utf-8') + content
    except FileNotFoundError:
        response = b"HTTP/1.1 404 Not Found\r\n\r\n404 Not Found"

    client_socket.sendall(response)
    client_socket.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server in ascolto su http://{HOST}:{PORT}")

    while True:
        client_conn, _ = server.accept()
        handle_request(client_conn)
