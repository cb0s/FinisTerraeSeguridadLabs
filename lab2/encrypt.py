"""
This is the encryption script. Run it with "python encrypt.py" (minimal python version: Python 3.8)
It encrypts a prior defined message (MSG) with ceaser encryption and
  Viginere with a prior defined password (PWD).
 After encryption, the message is hashed with the popular and secure SHA256 algorithm, which is already
  implemented into the standard libraries of Python.
 The encrypted message and optionally the hash (set with SAVE_WITH_HASH) are then saved to a JSON file
  at the given location (FILE_PATH).
  (Saving the hash in the same file like the message defeats the purpose of the hashing and is only
  integrated for demonstration purposes!)
 Finally all results are printed to the screen to be further used in other scripts and/or for debugging
  purposes.
The decryption script (decrypt.py) can recreate the original message, if the correct password and the
 hash of the message are correctly specified.

Eso es la solucion de Belen Rojas, Roberto Pineda, Cedric Boes para Lab 2 de Seguridad Informatica.
"""
# Own Imports
import cipher
import persistent


PWD = "securePassword"          # password for the Viginere encryption algorithm
MSG = "WhatALovelyMessageToSendThroughEncryptionAndDecryption" # msg to encrypt
FILE_PATH = "persistent.json"   # file path where to save the encrypted message (and optionally the hash)
SAVE_WITH_HASH = False          # if set to True, the messages sha256 hash is also saved


def main():
    l_just_const = 32
    print("Original Message:".ljust(l_just_const), MSG)
    
    print("---------------- Encrypting ----------------")
    # Encrypting Message
    enc_msg = cipher.rot(MSG, 4)
    enc_msg = cipher.Viginere(PWD).encrypt(enc_msg)
    enc_msg = cipher.rot(enc_msg, 16)

    # Hashing Message
    enc_hash = cipher.hash_256(enc_msg)
    print("Encrypted Message:".ljust(l_just_const), enc_msg)
    print("Hash of encrypted message:".ljust(l_just_const), enc_hash)

    print("-------------- Saving to file --------------")
    # Saves the encrypted message (and optionally the hash) to a prior defined file path
    # The output format of this file is JSON for easier debugging and because of it's perfect
    #  support in Python.
    persistent.save(FILE_PATH, enc_msg, enc_hash if SAVE_WITH_HASH else None)
    print("Saved successfully to '", FILE_PATH, "'", sep="")


if __name__ == '__main__':
    main()  # We are good programmers and use a main method as every Python-Programmer is supposed to :)
