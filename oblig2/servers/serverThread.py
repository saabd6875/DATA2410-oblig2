import socket
import threading

def handle_request(client_connection):
    """Behandler en HTTP-forespørsel i en egen tråd."""
    try:
        request = client_connection.recv(1024).decode()
        print("HTTP Request:\n", request)

        # Hent ut den forespurte filen
        requested_file = request.split()[1][1:]
        if requested_file == "":
            requested_file = "index.html"

        try:
            with open(requested_file, "r") as f:
                content = f.read()
            response = "HTTP/1.1 200 OK\r\n\r\n" + content
        except FileNotFoundError:
            response = "HTTP/1.1 404 Not Found\r\n\r\nFile Not Found"

        client_connection.sendall(response.encode())

    except Exception as e:
        print(f"Feil: {e}")

    finally:
        client_connection.close()

def start_server(port=8000):
    """Starter en multithreaded webserver."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)
    print(f"Server kjører på port {port}...")

    while True:
        client_connection, client_address = server_socket.accept()
        print(f"Tilkobling fra {client_address}")

        # Start en ny tråd for hver klient
        client_thread = threading.Thread(target=handle_request, args=(client_connection,))
        client_thread.start()

if __name__ == "__main__":
    start_server()
