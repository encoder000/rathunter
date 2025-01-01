import sys
sys.path.append('lib/jproto')
from jproto import *
import hashlib
import base64
import gzip

from Crypto.Cipher import AES

#FAGGOT BYTES
def get_local_encryption_key(obfus_key):
    ek = bytes.fromhex(
        hashlib.md5(obfus_key).hexdigest())
    ek = ek[0:15]+ek+b'\x00' #shitty virus problems lol

    #byte[] keyarray = new byte[32];                 -> keyarray = [0]*32
    #Array.Copy(mutexhash, 0, keyarray, 0, 16);      -> keyarray[0:16] = mutexhash[0:16]
    #Array.Copy(mutexhash, 0, keyarray, 15, 16);     -> keyarray[15:31]= mutexhash[0:16]
    
    return AES.new(ek, AES.MODE_ECB)

def compress(data):
    return int.to_bytes(len(data),4,'little')+gzip.compress(data)

def decompress(data):
    return gzip.decompress(data[4:])

def byte_cer(data):
    return base64.b64encode(compress(data))


