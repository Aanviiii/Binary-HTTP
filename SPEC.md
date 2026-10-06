# Binary HTTP Protocol (BHTTP) Version 1

## 1. Introduction

Binary HTTP Protocol (BHTTP) is a custom application-layer protocol implemented on top of TCP.

The objective of BHTTP is to retrieve files from a server using binary frames rather than traditional text-based HTTP messages.

Unlike HTTP, which relies on textual request and response messages, BHTTP uses compact fixed-size binary headers followed by variable-length payloads.

The protocol supports:

* File retrieval
* Persistent TCP connections
* Multiple requests on a single connection
* Binary framing
* Protocol versioning
* Future extensibility
* Error handling

---

# 2. Design Goals

The protocol was designed with the following goals:

1. Simplicity of implementation.
2. Easy frame parsing.
3. Persistent communication over a single TCP connection.
4. Separation of control information and payload data.
5. Extensibility for future protocol versions.
6. Efficient binary transmission.

---

# 3. Transport Layer

BHTTP operates on top of TCP.

TCP was selected because it provides:

* Reliable delivery
* Ordered delivery
* Error detection
* Stream-oriented communication

Since TCP guarantees ordered delivery, BHTTP does not require sequence numbers or retransmission mechanisms.

---

# 4. Byte Order

All multi-byte integer fields use:

```text
Network Byte Order (Big Endian)
```

This is consistent with standard Internet protocols.

Example:

```text
200 decimal

00 C8 hexadecimal
```

---

# 5. Protocol Version

Every frame begins with a protocol version field.

Current Version:

```text
1
```

Future versions may extend the protocol while preserving backward compatibility.

---

# 6. Request Frame Format

A request frame consists of a fixed-size 8-byte header followed by a payload.

## Request Header Layout

| Field          | Size    |
| -------------- | ------- |
| Version        | 1 byte  |
| Frame Type     | 1 byte  |
| Flags          | 1 byte  |
| Reserved       | 1 byte  |
| Payload Length | 4 bytes |

Total Header Size:

```text
8 bytes
```

---

## Field Descriptions

### Version

Protocol version number.

Current value:

```text
1
```

---

### Frame Type

Identifies the type of request.

| Value | Meaning     |
| ----- | ----------- |
| 1     | GET_REQUEST |
| 3     | PING        |

---

### Flags

Reserved for future protocol extensions.

Current value:

```text
0
```

---

### Reserved

Reserved for future use.

Current value:

```text
0
```

---

### Payload Length

Length of the payload in bytes.

Maximum supported payload size:

```text
4096 bytes
```

---

## Request Payload

The request payload contains a UTF-8 encoded file path.

Example:

```text
/index.html
```

---

# 7. Response Frame Format

A response frame consists of a fixed-size 12-byte header followed by response headers and body content.

## Response Header Layout

| Field         | Size    |
| ------------- | ------- |
| Version       | 1 byte  |
| Frame Type    | 1 byte  |
| Status Code   | 2 bytes |
| Header Length | 4 bytes |
| Body Length   | 4 bytes |

Total Header Size:

```text
12 bytes
```

---

## Response Headers

Headers are UTF-8 encoded metadata.

Example:

```text
Content-Type:text/html
```

Header Length specifies the number of bytes occupied by the header section.

---

## Response Body

Contains the requested file contents.

The body may contain:

* HTML files
* Text files
* Images
* Binary files

The receiver uses Body Length to determine where the body ends.

---

# 8. Status Codes

The protocol defines three status codes.

| Code | Meaning     |
| ---- | ----------- |
| 200  | OK          |
| 400  | BAD REQUEST |
| 404  | NOT FOUND   |

---

## 200 OK

Returned when the requested file exists and is successfully transmitted.

---

## 400 BAD REQUEST

Returned when:

* Invalid protocol version
* Invalid UTF-8 payload
* Payload exceeds maximum size
* Path validation fails
* Malformed request frame

---

## 404 NOT FOUND

Returned when the requested file does not exist inside the document root.

---

# 9. Persistent Connections

A TCP connection remains open after a response is sent.

The client may transmit multiple requests using the same connection.

Example:

```text
Connect

GET /index.html

GET /about.html

GET /test.txt

Disconnect
```

Only one TCP connection is created.

This reduces connection setup overhead and improves efficiency.

---

# 10. PING Frames

The protocol includes a PING frame type.

PING frames may be used to verify connectivity without requesting a file.

Request:

```text
Frame Type = 3
```

Response:

```text
Status = 200
Body = PONG
```

---

# 11. Unknown Frame Handling

Unknown frame types must not terminate the connection.

When an unknown frame type is received:

1. Read the payload length.
2. Consume the payload.
3. Ignore the frame.
4. Continue processing future frames.

This design allows future protocol extensions without breaking existing implementations.

---

# 12. Security

The server restricts access to files located inside the configured document root.

Path validation uses:

```text
realpath()
commonpath()
```

to prevent directory traversal attacks.

Example of rejected request:

```text
../../../Windows/System32
```

The server responds:

```text
400 BAD REQUEST
```

---

# 13. Error Handling

The server attempts to continue serving requests whenever possible.

Invalid requests generate error responses rather than immediately terminating the TCP connection.

This improves robustness and protocol stability.

---

# 14. Design Decisions

### Fixed-Size Headers

Fixed-size headers simplify parsing because the receiver always knows how many bytes must be read before processing a frame.

---

### Length-Prefixed Payloads

Payload lengths eliminate delimiter ambiguity and allow binary content to be transmitted safely.

---

### Persistent Connections

Reusing a single TCP connection reduces connection establishment overhead and improves efficiency.

---

### Binary Framing

Binary framing reduces protocol overhead compared with text-based parsing.

---

### Version Field

Versioning allows future protocol revisions without changing the basic communication model.

---

### Unknown Frame Skipping

Ignoring unknown frame types improves forward compatibility and protocol extensibility.

---

# 15. Conclusion

BHTTP is a lightweight binary file-transfer protocol built on TCP.

The protocol demonstrates:

* Custom protocol design
* Binary framing
* Persistent communication
* Error handling
* Security validation
* Extensible architecture

while remaining simple enough to implement and test in a Network Architecture project.
