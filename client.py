import socket
import struct
import sys

from protocol import *


def recv_exact(sock, size):

    data = b""

    while len(data) < size:

        chunk = sock.recv(
            size - len(data)
        )

        if not chunk:
            raise ConnectionError(
                "Connection closed"
            )

        data += chunk

    return data


def hexdump(data):

    for i in range(
        0,
        len(data),
        16
    ):

        chunk = data[i:i + 16]

        hex_values = " ".join(
            f"{b:02x}"
            for b in chunk
        )

        print(
            f"{i:08x}  {hex_values}"
        )


def send_get(sock, path):

    payload = path.encode()

    frame = struct.pack(
        REQUEST_HEADER_FORMAT,
        VERSION,
        FRAME_GET,
        0,
        0,
        len(payload)
    )

    print("\nREQUEST FRAME\n")

    hexdump(
        frame + payload
    )

    sock.sendall(frame)
    sock.sendall(payload)

    response_header = recv_exact(
        sock,
        RESPONSE_HEADER_SIZE
    )

    (
        version,
        frame_type,
        status,
        header_len,
        body_len
    ) = struct.unpack(
        RESPONSE_HEADER_FORMAT,
        response_header
    )

    headers = recv_exact(
        sock,
        header_len
    )

    body = recv_exact(
        sock,
        body_len
    )

    print("\nRESPONSE FRAME\n")

    hexdump(
        response_header +
        headers +
        body
    )

    print("\nSTATUS:", status)

    if body:
        print(
            body.decode(
                errors="ignore"
            )
        )

    return status


def main():

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.connect(
        ("localhost", 9000)
    )

    print(
        "Connected."
    )

    while True:

        path = input(
            "\nPath> "
        ).strip()

        if path.lower() == "quit":
            break

        status = send_get(
            sock,
            path
        )

        if status >= 400:
            print(
                "Server returned error."
            )

    sock.close()


if __name__ == "__main__":
    main()