import socket  # noqa: F401

def create_message(id):
    id_bytes = id.to_bytes(4, byteorder="big")
    return len(id_bytes).to_bytes(4, byteorder="big") + id_bytes

def handle_client(client):
    req = client.recv(1024)
    print(req)
    coRelationId = int.from_bytes(req[8:12], byteorder="big")

    if coRelationId > 4:
        raise Exception("Invalid coRelationId")

    client.sendall(create_message(coRelationId))
    client.close()

def main():
    print("Logs from your program will appear here!")

    server = socket.create_server(("localhost", 9092), reuse_port=True)

    while True:
        client, addr = server.accept()
        handle_client(client)


if __name__ == "__main__":
    main()