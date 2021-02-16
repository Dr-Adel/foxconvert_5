__author__ = 'Dr Adel'
__creation__ = '22/06/2016'
__location__ = 'Roushdy'
__update_1__ = '13/2/2018'
__last_update__ = '14/3/2020'

# package name: pycrypto

from Crypto.Cipher import AES
import math


dbconnection = {'host': '127.0.0.1', 'database': 'zakah', 'user': 'postgres', 'password': 'root'}
FIRST_GRP = {'grpname': 'admin', 'privelage_read': 'y', 'privelage_write': 'y'}
FIRST_USER = {'username': 'supervisor', 'groups': ['admin', ]}

""" Encrypts plain text (strings):
to change from dict to string : use repr(dict)
to convert back after decryption: use eval(str)
repr(dictionary) -> enc -> save as binary -> read from binary -> dec -> eval(dec)
"""

def cipher():
    '''https://pypi.python.org/pypi/pycrypto key, mode, IV'''
    # return AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    return AES.new(b'AlWardGameel1234', AES.MODE_CBC, b'GameelAlward7890')


def enc(pw):
    '''encrypt a plain text string'''
    # plaintext must be multiple of 16 bytes
    width = 16 * math.ceil(len(pw) / 16)
    pw = pw.ljust(width)
    obj = cipher()
    return obj.encrypt(bytes(pw,'utf-8'))


def dec(hash):
    '''decrypt to bytes, must use same key and IV'''
    obj = cipher()
    # convert to string and strip extra spaces
    return obj.decrypt(hash).decode('utf8').strip()


def encode_values(dict):
    '''encoding all values of any dictionary using dictionary comprehension'''
    # returns a dictionary where all values are encrypted
    return {x: enc(dict[x]) for x in dict.keys()}


def decode_values(dict):
    '''decoding all values of any dictionary using dictionary comprehension'''
    # returns a decrypted dictionary
    return {x: dec(dict[x]) for x in dict.keys()}

def encodeAll(dict):
    '''encoding all sets of any dictionary using dictionary comprehension'''
    # returns a dictionary where all values are encrypted
    return {enc(x): enc(dict[x]) for x in dict.keys()}


def decodeAll(dict):
    '''decoding all sets of any dictionary using dictionary comprehension'''
    # returns a decrypted dictionary
    return {dec(x): dec(dict[x]) for x in dict.keys()}


if __name__ == '__main__':
    e = encodeAll(dbconnection)
    print(e)
    f = decodeAll(e)
    print(f)

