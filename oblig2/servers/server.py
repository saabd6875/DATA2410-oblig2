import socket


def handle_request(client_connection):
    """Behandler en HTTP-forespørsel fra en klient."""
    request = client_connection.recv(1024).decode()
    print("HTTP Request:\n", request)

    # Hent ut den forespurte filen (f.eks. GET /index.html HTTP/1.1)
    try:
        requested_file = request.split()[1][1:]  # Fjern "/" fra "/index.html"
        if requested_file == "":
            requested_file = "index.html"  # Standardfil hvis ingen fil er spesifisert
        
        with open(requested_file, "r") as f:
            content = f.read()
        
        # Lag en HTTP 200 OK-respons
        response = "HTTP/1.1 200 OK\n\n" + content

    except FileNotFoundError:
        # Returner en HTTP 404 Not Found-melding
        response = "HTTP/1.1 404 Not Found\n\nFile Not Found"

    # Send respons til klienten
    client_connection.sendall(response.encode())
    client_connection.close()

def start_server(port=8000):
    """Starter en enkel webserver som lytter på porten."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))  # Lytt på alle IP-er på denne maskinen
    server_socket.listen(5)  # Maks 5 ventende forbindelser
    print(f"Serveren kjører på port {port}...")

    while True:
        client_connection, client_address = server_socket.accept()
        print(f"Tilkobling fra {client_address}")
        handle_request(client_connection)

if __name__ == "__main__":
    start_server()
