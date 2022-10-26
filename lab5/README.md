# Documentation

## Message Format

This implementation uses a simple, yet effective, custom message format. It is used to determine in which state the algorithm is and which algorithms to use in the encryption process.
It can also be used to either switch the encryption technique or to create a new secret key for the existing connection.
In this message format, the client creates requests. This means all the communication is controlled by the client and therefore only the server needs to interpret message flags. In case of errors the server just closes the connection.

### Specification

1. Message-Flag byte to specify the current state of the connection [1 Byte]
2. Depending on the state, an additional fixed amount of additional flag bytes [0-2 Bytes]
3. Payload in JSON format [no limit]

### Key Exchange state

In the key exchange state, a random key is exchanged with a specified algorithm (currently only Diffie Hellman). This key can then be used by a symmetric encryption algorithm specified by the correct Encryption-Flag.
If no encryption is desired, the key-exchange algorithm must be set to the `NO_ENC` Encryption-Flag.

### Operation state

In this state, messages are sent with the specified encryption method. By default, no encryption is applied and the message is sent in plain text.

## Dependencies and Versions

This project uses barely any external dependencies apart from the encryption library _pycryptodome_ (tested version v3.15.0).
It can be installed using the packet-manager pip:

```bash
pip install pycryptodome
```

All scripts were tested on a Windows 10 Host-System with CPython 3.8.5.
