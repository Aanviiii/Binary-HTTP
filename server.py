import os
import socket
import struct
import mimetypes
import sys

from protocol import *

HOST = "0.0.0.0"
PORT = 9000
ROOT = os.path.realpath("./www")


def recv_exact(conn, size):

    data = b""

    while len(data) < size:

        chunk = conn.recv(size - len(data))

        if not chunk:
            return None

        data += chunk

    return data


def send_response(conn, status, headers, body):

    header_bytes = headers.encode("utf-8")

    frame = struct.pack(
        RESPONSE_HEADER_FORMAT,
        VERSION,
        FRAME_RESPONSE,
        status,
        len(header_bytes),
        len(body),
    )

    conn.sendall(frame)
    conn.sendall(header_bytes)
    conn.sendall(body)


def safe_path(path):

    requested = path.lstrip("/")

    full_path = os.path.realpath(
        os.path.join(ROOT, requested)
    )

    try:
        return (
            os.path.commonpath(
                [ROOT, full_path]
            )
            == ROOT
        )
    except ValueError:
        return False


def build_file_response(path):

    if not safe_path(path):

        return (
            STATUS_BAD_REQUEST,
            "Content-Type:text/plain",
            b"Invalid Path",
        )

    requested = path.lstrip("/")

    full_path = os.path.realpath(
        os.path.join(ROOT, requested)
    )

    if not os.path.isfile(full_path):

        return (
            STATUS_NOT_FOUND,
            "Content-Type:text/plain",
            b"File Not Found",
        )

    with open(full_path, "rb") as f:
        body = f.read()

    content_type = (
        mimetypes.guess_type(full_path)[0]
        or "application/octet-stream"
    )

    headers = f"Content-Type:{content_type}"

    return (
        STATUS_OK,
        headers,
        body,
    )


def handle_frame(conn):

    header = recv_exact(
        conn,
        REQUEST_HEADER_SIZE,
    )

    if not header:
        return False

    (
        version,
        frame_type,
        flags,
        reserved,
        payload_length,
    ) = struct.unpack(
        REQUEST_HEADER_FORMAT,
        header,
    )

    if payload_length > MAX_PAYLOAD_SIZE:

        payload = recv_exact(
            conn,
            payload_length,
        )

        send_response(
            conn,
            STATUS_BAD_REQUEST,
            "",
            b"Payload Too Large",
        )

        return True

    payload = recv_exact(
        conn,
        payload_length,
    )

    if payload is None:
        return False

    if version != VERSION:

        send_response(
            conn,
            STATUS_BAD_REQUEST,
            "",
            b"Unsupported Version",
        )

        return True

    if frame_type == FRAME_PING:

        send_response(
            conn,
            STATUS_OK,
            "",
            b"PONG",
        )

        return True

    if frame_type != FRAME_GET:

        print(
            f"Skipping unknown frame type {frame_type}"
        )

        return True

    try:

        path = payload.decode(
            "utf-8"
        )

    except UnicodeDecodeError:

        send_response(
            conn,
            STATUS_BAD_REQUEST,
            "",
            b"Bad UTF-8",
        )

        return True

    status, headers, body = (
        build_file_response(path)
    )

    send_response(
        conn,
        status,
        headers,
        body,
    )

    return True


def main():

    host = HOST
    port = PORT

    if len(sys.argv) >= 2:
        port = int(sys.argv[1])

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1,
    )

    server.bind((host, port))
    server.listen()

    print(
        f"BHTTP Server Listening on {port}"
    )

    while True:

        conn, addr = server.accept()

        print(
            f"Connected: {addr}"
        )

        try:

            while handle_frame(conn):
                pass

        except Exception as e:

            print("Error:", e)

        finally:

            conn.close()


if __name__ == "__main__":
    main()