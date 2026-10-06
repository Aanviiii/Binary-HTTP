# Binary HTTP Protocol (BHTTP) Version 1

## 1. Introduction

Binary HTTP (BHTTP) is a lightweight application-layer protocol implemented on top of TCP.

The goal of the protocol is to transfer files using binary frames instead of text-based HTTP messages.

The protocol supports:

* Persistent TCP connections
* Multiple requests on a single connection
* Binary frame headers
* File retrieval
* Versioning
* Future extensibility

---

# 2. Request Frame Format

Request frames use a fixed-size 8-byte header.

| Field          | Size    |
| -------------- | ------- |
| Version        | 1 byte  |
| Frame Type     | 1 byte  |
| Flags          | 1 byte  |
| Reserved       | 1 byte  |
| Payload Length | 4 bytes |

Payload contains the requested file path encoded using UTF-8.

Example payload:

```text
/index.html
```

---

# 3. Response Frame Format

Response frames use a fixed-size 12-byte header.

| Field         | Size    |
| ------------- | ------- |
| Version       | 1 byte  |
| Frame Type    | 1 byte  |
| Status Code   | 2 bytes |
| Header Length | 4 bytes |
| Body Length   | 4 bytes |

Response payload consists of:

1. Response headers
2. File content

---

# 4. Frame Types

| Value | Meaning     |
| ----- | ----------- |
| 1     | GET_REQUEST |
| 2     | RESPONSE    |
| 3     | PING        |

Future frame types may be added without breaking compatibility.

---

# 5. Status Codes

| Code | Meaning     |
| ---- | ----------- |
| 200  | OK          |
| 400  | BAD REQUEST |
| 404  | NOT FOUND   |

---

# 6. Persistent Connections

The server keeps the TCP connection open after sending a response.

The client may send multiple requests over the same connection.

This reduces connection setup overhead and improves efficiency.

---

# 7. Unknown Frame Handling

Unknown frame types are skipped.

The server reads the payload length, discards the payload, and continues processing future frames.

This allows future protocol extensions.

---

# 8. Security

The server prevents directory traversal attacks.

Requests attempting to access files outside the document root are rejected with a 400 response.

Example:

```text
../../../Windows/System32
```

---

# 9. Versioning

Version field allows future protocol revisions.

Current protocol version:

```text
1
```

Future implementations may support newer versions while maintaining backward compatibility.

---

# 10. Design Decisions

1. Fixed-size headers simplify parsing.
2. Length-prefixed payloads avoid delimiter issues.
3. Persistent connections improve performance.
4. Binary framing reduces protocol overhead.
5. Unknown frame skipping enables extensibility.
