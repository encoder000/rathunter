import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import threading
import traceback

pygame.init()

def thread_proxy(func,config,io,args,cmds):
    try:
        func(config,io,args,cmds)
    except:
        io.log_win.print(traceback.format_exc())


def beep(config,io,args,cmds):
    '''
Just beep lol<3
    '''
    beep_sound = pygame.mixer.Sound('resources/beep.mp3') 
    beep_sound.play()

def run_thread(config,io,args,cmds):
    '''
Run function in thread
This will deattach proccess from
console blocking
(works only with functions, not modules)
    '''
    if not args[0] in cmds:
        io.term_win.print('Cant find this function')
        return
    
    if not cmds[args[0]]:
        io.term_win.print("Looks like pseudo-function. Cant run it in thread")
        return

    if not isinstance(cmds[args[0]],dict):
        io.term_win.print("This doesn't look lile function.\nMaybe its module?")
        return
    
    if "arglen" in cmds[args[0]]:
        if not io.check_arg_len(args,cmds[args[0]]["arglen"]):
            return

    if "config_args" in cmds[args[0]]:
        for i in cmds[args[0]]["config_args"]:
            io.check_arg(i,config)
    
    threading.Thread(target=thread_proxy,
                     args=(cmds[args[0]]['f'],config,io,args[1:],cmds)).start()

funcs = {"beep":{'f':beep},"&":{'f':run_thread,'arglen':1}}
