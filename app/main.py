import socket  # noqa: F401

def create_message(id):
    id_bytes = id.to_bytes(4, byteorder="big")
    return len(id_bytes).to_bytes(4, byteorder="big") + id_bytes

def create_error_message(coRelationId, error_code):
    message = coRelationId.to_bytes(4, byteorder="big") + error_code.to_bytes(2, byteorder="big")
    return len(message).to_bytes(4, byteorder="big") + message

def handle_client(client):
    req = client.recv(1024)
    acceptApiVersion = [0,1,2,3,4]
    api_version = int.from_bytes(req[6:8], byteorder="big")
    coRelationId = int.from_bytes(req[8:12], byteorder="big")

    if api_version not in acceptApiVersion:
        print('api_version not in acceptApiVersion')
        error_code = 35
        client.sendall(create_error_message(coRelationId, error_code))
        client.close()
        return

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