import socket  # noqa: F401

def check_api_version(api_version):
    acceptApiVersion = [0, 1, 2, 3, 4]
    if api_version not in acceptApiVersion:
        print('API version not supported')
        return 35
    return 0


def create_message(coRelationId, api_key, error_code):
    response_header = coRelationId.to_bytes(4)

    min_version = 0
    max_version = 4
    tag_buffer = b"\x00"
    throttle_time_ms = 0

    response_body = (
        error_code.to_bytes(2)
        + int(2).to_bytes(1)
        + api_key.to_bytes(2)
        + min_version.to_bytes(2)
        + max_version.to_bytes(2)
        + tag_buffer
        + throttle_time_ms.to_bytes(4)
        +tag_buffer
    )

    response_lenght = len(response_header) + len(response_body)
    return response_lenght.to_bytes(4) + response_header + response_body


def handle_client(client):
    req = client.recv(1024)
    error_code = check_api_version(int.from_bytes(req[6:8], byteorder="big"))
    api_key = int.from_bytes(req[4:6], byteorder="big")
    coRelationId = int.from_bytes(req[8:12], byteorder="big")

    client.sendall(create_message(coRelationId, api_key, error_code))


def main():
    print("Logs from your program will appear here!")

    server = socket.create_server(("localhost", 9092), reuse_port=True)

    while True:
        client, addr = server.accept()
        handle_client(client)

if __name__ == "__main__":
    main()