# Annotated Hexdump

## Request

Client requests:

```text
/index.html
```

Raw Bytes:

```text
01 01 00 00 00 00 00 0b
2f 69 6e 64 65 78 2e 68 74 6d 6c
```

Explanation:

```text
01
Version = 1

01
Frame Type = GET_REQUEST

00
Flags

00
Reserved

00 00 00 0b
Payload Length = 11

2f 69 6e 64 65 78 2e 68 74 6d 6c
"/index.html"
```

---

## Response

Example Response:

```text
Status = 200
```

Raw Header:

```text
01 02 00 c8 00 00 00 16 00 00 00 1a
```

Explanation:

```text
01
Version = 1

02
Frame Type = RESPONSE

00 c8
Status = 200

00 00 00 16
Header Length = 22

00 00 00 1a
Body Length = 26
```

---

## Status Examples

```text
200 = OK
400 = BAD REQUEST
404 = NOT FOUND
```

---

## Example Error Response

Request:

```text
/does_not_exist.html
```

Response:

```text
404 NOT FOUND
```

The response body contains:

```text
File Not Found
```
