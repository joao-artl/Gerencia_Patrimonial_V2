import socket
import time
import os

host = os.environ.get("API_HOST", "localhost")
port = int(os.environ.get("API_PORT", 8000))
timeout = 1

print(f"Aguardando pelo serviço em http://{host}:{port}...")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect((host, port))
        s.close()
        print("Serviço está pronto!")
        break
    except socket.error as ex:
        print(f"Serviço ainda não está pronto, tentando novamente em {timeout} segundo(s)...")
        time.sleep(timeout)