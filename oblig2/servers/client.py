import socket
import argparse

def send_request(server_ip, port, filename):
    """Sender en HTTP GET-forespørsel til serveren og mottar responsen."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, port))

        # Konstruer HTTP-forespørselen
        request = f"GET /{filename} HTTP/1.1\r\nHost: {server_ip}\r\n\r\n"
        client_socket.sendall(request.encode())

        # Motta respons fra serveren

        response = b""
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            response += chunk

        print("Server response:\n", response.decode(errors="ignore"))

    except Exception as e:
        print(f"Feil under kommunikasjon: {e}")

    finally:
        client_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTTP-klient for testing")
    parser.add_argument("-i", "--ip", required=True, help="Serverens IP-adresse")
    parser.add_argument("-p", "--port", type=int, required=True, help="Portnummer")
    parser.add_argument("-f", "--file", required=True, help="Fil som skal hentes")

    args = parser.parse_args()
    send_request(args.ip, args.port, args.file)
