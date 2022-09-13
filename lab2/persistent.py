"""
File handling module saving and loading the encrypted message,
optionally with its corresponding hash.

For easier debugging, JSON is used as the file format.

Note: This is a library and is not supposed to run as a standalone application.
"""
import json
from typing import Tuple, Union


def save(file_p, enc_msg, enc_hash=None):
    file_content = {
        'msg': enc_msg
    }
    if enc_hash is not None:
        file_content['hash'] = enc_hash

    with open(file_p, 'w') as json_file:
        json.dump(file_content, json_file, indent=4)


def load(file_p) -> Tuple[str, Union[str, None]]:
    with open(file_p, 'r') as json_file:
        file_content = json.load(json_file)
    
    return file_content['msg'], file_content.get('hash', None)
