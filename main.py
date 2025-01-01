import time

from lib import ui
from lib import config
from lib import default_funcs

import root_module
import sys
import traceback
import curses

def read_modstack(root,modstack):
    for i in modstack:
        root = root.submodules[i]
    return root

io  = ui.ui()

term= io.term_win
modstack = []
conf     = {}

io.config_win.config_print(conf)
h, w = io.scr.getmaxyx()

term.print("Hiii,welcome to RAT-HUNTER by encoder000 t.me/fox_society")
term.print('Use "help" to get comand list\n')


while True:
    instr = ['[>]']
    inp = term.input(instr+modstack).split(' ')
    if term.resized:
        term_text   = io.term_win.text[:-1]
        log_text    = io.log_win.text
        io.alive = False

        curses.endwin()
        io = ui.ui()
        io.term_win.text  = term_text
        io.log_win.text   = log_text
        io.log_win.print(end='')
        io.config_win.config_print(conf)

        term = io.term_win
        
    cmd,args = inp[0],inp[1:]
    
    commands = {'exit':None,'help':None,'cls':None}
    commands|= config.funcs
    commands|= default_funcs.funcs
    commands|= read_modstack(root_module,modstack).funcs
    commands|= read_modstack(root_module,modstack).submodules

    if cmd in commands:
        if cmd == 'exit':
            if not modstack:
                curses.nocbreak()
                io.scr.keypad(0)
                curses.echo()
                curses.endwin()
                sys.exit(0)
            else:
                del modstack[-1]

        elif cmd == 'help':
            if len(args) == 0:
                term.print(' '.join(list(commands.keys())))
            else:
                if len(args) == 1:
                    if not args[0] in commands.keys():
                        term.print('This function does not exist')
                    elif isinstance(commands[args[0]],dict):
                        if not commands[args[0]]['f'].__doc__:
                            term.print('There is no doc for this function')
                        else:
                            term.print(commands[args[0]]['f'].__doc__)
        elif cmd == "cls":
            io.scr.clear()
            io.init_windows()
            term = io.term_win
            
        else:
            try:
                if isinstance(commands[cmd],dict):
                    if "arglen" in commands[cmd].keys():
                        if not io.check_arg_len(args,commands[cmd]["arglen"]):
                            continue
                    if "config_args" in commands[cmd].keys():
                        for i in commands[cmd]["config_args"]:
                            io.check_arg(i,conf)
                        
                    commands[cmd]['f'](conf,io,args,commands)
                    io.config_win.config_print(conf)
                else:
                    modstack.append(cmd)
            except:
                io.log_win.print(traceback.format_exc())