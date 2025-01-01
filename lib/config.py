def config(config,io,args,cmds):
    '''
config setval key value
config delval key
config getval key
config clearconfig
    '''
    if args[0] == "setval":
        if io.check_arg_len(args,3):
            config[args[1]] = args[2]
    elif args[0] == "getval":
        if io.check_arg_len(args,2):
            io.term_win.print(config[args[1]])
    elif args[0] == "delval":
        if io.check_arg_len(args,2):
            del config[args[1]]
    elif args[0] == "clearconfig":
        config.clear()

funcs = {"config":{"f":config,"arglen":1,"config_args":[]}}
