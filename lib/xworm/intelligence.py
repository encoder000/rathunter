import re
from .helpers import *
import traceback

def check_string(str_):
    str_ += b'=='
    res = []
    for i in range(len(str_)):
        try:
            e = base64.b64decode(str_[i:])
            if len(e)%16==0 and len(e) != 0:
                res.append(e)
        except:pass
    return res

def scan(config,io,args,cmds):
    '''
Scans xworm PE and decrypts config
E.g "scanfile samples/XClient.exe"
    '''
    if io.check_arg_len(args,1):
        log      = io.log_win
        filename = args[0]

        regex = re.compile(rb'[\x00a-zA-Z0-9/\+=]{16,}')
        data = open(filename,'rb').read().replace(b'\x00',b'')
        blacklist = [b'AntivirusProduct',b'GenericMicrosoft',
                 b'manifestVersion=',b'STATESendMSGHget',
                 b'assemblyIdentity',b'ExplicitSplitset',
                 b'DrawingToLongset',b'WorkingDirectory',
                 b'ExclusionProcess']
        config_strings = []
        maybe_keys = []

        for i in regex.findall(data):
            if len(i) == 16:
                if not i in blacklist:
                    maybe_keys.append(get_local_encryption_key(i))

            elif b'==' in i:
                config_strings += i.split(b'=')

        for i in config_strings:
            c = check_string(i)
            for j in c:
                for key in maybe_keys:
                    try:
                        log.print('|-',key.decrypt(j))
                    except:
                        pass

        while True:
            in_ = io.term_win.input(
                "Do you have other yummy base64 strings(press enter to skip> ")
            if not in_:
                break
            log.print(key.decrypt(base64.b64decode(in_)))
