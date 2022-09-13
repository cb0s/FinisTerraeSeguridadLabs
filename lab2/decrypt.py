"""
This is the decryption script. Run it with "python decrypt.py" (minimal python version: Python 3.8)
Loads a persistently saved message (and optionally its corresponding hash -> dangerous in real life,
  just for demonstration purposes) from a prior created JSON file at the specified path (FILE_PATH).
  (To create such a JSON file run the encryption script first!)
 If the hash is not saved together with the file (recommended), the user is prompted to enter the
  correct SHA-256 hash of the message.
 In the case the hash matches the calculated hash of the loaded message, the decryption continues.
 Otherwise the application exits with an error message, telling that the message appears to tampered.
 The decryption combines a reverse Caeser encryption (decryption) with the Viginere algorithm with a
  given password (PWD).
 After decryption, the original message is printed out on the console.
The encryption script (encrypt.py) can create the required persistent JSON file, if the correct password
 message are correctly specified.

Eso es la solucion de Belen Rojas, Roberto Pineda, Cedric Boes para Lab 2 de Seguridad Informatica.
"""
import sys
import cipher
import persistent


PWD = "securePassword"
FILE_PATH = "persistent.json"


def main():
    l_just_const = 32

    # Loading persistently saved message (and optionally the hash) from file
    print("------------ Loading from file -------------")
    enc_msg, enc_hash = persistent.load(FILE_PATH)
    print(f"File contents of '{FILE_PATH}' loaded")
    print("Encrypted Message:".ljust(l_just_const), enc_msg, sep="")

    if enc_hash is None:
        # In this case the hash was not included in the file
        enc_hash = input("Enter hash of msg:".ljust(l_just_const))
    else:
        # Here the hash was included in the persistent log
        print("Hash of encrypted message:".ljust(l_just_const), enc_hash, sep="")
    
    # Checking if given hash matches the calculated hash of the loaded message
    if enc_hash != (calculated_hash := cipher.hash_256(enc_msg)):
        print(f"""Message appears to be tampered!
Supposed hash '{enc_hash}' of encrypted message does \
not match the actual messages hash '{calculated_hash}'""",
            sep="",
            file=sys.stderr
        )
        exit(1)
    
    print("Given hash and hash of message match!")

    # Decryption with reverse Caeser Rotation encryption and Viginere 
    print("---------------- Decrypting ----------------")
    dec_msg = cipher.rot(enc_msg, -16)
    dec_msg = cipher.Viginere(PWD).decrypt(dec_msg)
    dec_msg = cipher.rot(dec_msg, -4)

    # Printing out the decrypted message - and we are finally done :D
    print("Decrypted Message:".ljust(l_just_const), dec_msg, sep="")


if __name__ == '__main__':
    main()  # We are good programmers and use a main method as every Python-Programmer is supposed to :)
