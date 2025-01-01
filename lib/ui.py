import curses
import time
import threading

class winbox:
    def __init__(self,y,x,by,bx,name,screen,defcol):
        self.win  = curses.newwin(y,x,by,bx)
        self.y    = y
        self.x    = x
        self.by   = by
        self.bx   = bx
        self.name = name
        self.scr  = screen
        self.col  = defcol
        
        self.text    = []
        self.cur     = [1,1] #y,x
        self.history =[]
        self.resized = False
        self.refreshed=False

        self.win.keypad(True)
        self.win.box()
        self.win.addstr(0,x//2-len(name)//2,name, curses.color_pair(1))

        self.win.refresh()

    def print(self,*data,end='\n',join=' '):
        data = join.join(map(str,data))+end

        text = ''.join(self.text)+data
        lastchunk = '' 
        self.text = []
        
        for i in text:
            if i == '\n':
                self.text.append(lastchunk+'\n')
                lastchunk = ''
            elif len(lastchunk)==self.x-3:
                self.text.append(lastchunk)
                lastchunk = i
            else:
                lastchunk+= i
                
        if len(lastchunk) != 0:
            self.text.append(lastchunk)

        for i in range(len(self.text)-self.y+2):
            del self.text[0]
            
        self.refresh()
                    

    def config_print(self,config):
        self.win.clear()
        self.text = []
        
        self.print(' '.join(config.keys()))

    def input(self,in_='',join='>',end='>> '):
        if len(self.text) >= self.y-2:
            del self.text[0]

        if isinstance(in_,list):
            in_ = join.join(in_)+end
        
        self.print(in_,end='')
        self.history.append('')

        hindex = len(self.history)-1
        res = ''
        old_text = self.text
        
        while True:
            k = self.win.get_wch(*self.cur)
            if k == '\n':
                break
            elif k == curses.KEY_UP:
                if hindex >= 0:
                    hindex -= 1
                    res = self.history[hindex]
                
            elif k == curses.KEY_DOWN:
                if hindex < len(self.history)-1:
                    hindex += 1
                    res = self.history[hindex]
                    
            elif k == curses.KEY_BACKSPACE:
                res = res[:-1]
            elif k == curses.KEY_RESIZE:
                self.resized = True
                self.text = old_text
                break
            else:
                if k != curses.KEY_LEFT and k != curses.KEY_RIGHT:
                    res += k
                    
            self.print(res,end='')
            self.text = old_text
        
        if self.text:
            self.text[-1] += res+'\n'
        else:
            self.text.append(res+'\n')

        if res:
            if len(self.history) >= 2:
                if res == self.history[-2]:
                    del self.history[-1]
                    return res
            self.history[-1] = res
            
        else:
            del self.history[-1]
            
        return res

    def refresh(self):
        self.win.clear()
        
        for e,i in enumerate(self.text):
            self.win.addstr(1+e,1,i,curses.color_pair(self.col))
            self.cur[1] = len(i)+1

            if self.text:
                if self.text[-1].endswith('\n'):
                    self.cur[1] = 1
            
        self.cur[0] = len(self.text)
        self.win.box()
        self.win.addstr(0,self.x//2-len(self.name)//2,
                        self.name, curses.color_pair(1))
        self.refreshed = True
    
class ui:
    def __init__(self):
        self.scr = curses.initscr()
        curses.noecho()
        curses.start_color()
        self.alive = True

        curses.init_color(100,100, 1000, 500) #green
        curses.init_color(0, 0, 0, 0)         #black
        curses.init_color(101, 996, 839, 0)   #golden

        curses.init_pair(1, 100, curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)
        curses.init_pair(3,curses.COLOR_GREEN,curses.COLOR_BLACK)
        curses.init_pair(4, 101, curses.COLOR_BLACK)

        self.init_windows()

    def init_windows(self):
        self.y,self.x = self.scr.getmaxyx()
        
        self.config_win = winbox(5,self.x,0,0,'CONFIG',self.scr,1)
        self.term_win  = winbox(self.y-5,self.x//2,5,0,'TERMINAL',self.scr,0)
        self.log_win  = winbox(self.y-5,self.x//2,5,self.x//2,'LOG',self.scr,4)
        self.windows = [self.config_win,self.term_win,self.log_win]

        threading.Thread(target=self.updater).start()# -> for future

    def check_arg(self,argname,config,in_=[],join='>',end='?> ',rep=None):
        if not argname in config.keys():
            if rep:
                config[argname] = rep
                self.log_win.print(f'Updated param {argname}:{rep}')
                return
            
            in_ = list(in_)+[argname]
            data = self.term_win.input(in_,join,end)
            config[argname] = data
            self.log_win.print(f'Updated param {argname}:{data}')
            
        self.config_win.config_print(config)

    def check_arg_len(self,args,len_):
        if len(args)<len_:
            self.term_win.print(f'Not enought args. Should be {len_} or more')
            self.term_win.print('To get more info about function use "help {funcname}"')
            return False
        return True
    
    def updater(self):
        while self.alive:
            for win in [self.log_win,self.config_win]:
                if win.refreshed:
                    time.sleep(0.2)
                    if self.alive:
                        win.win.refresh()
                        win.refreshed = False
                    else:
                        break

            #self.scr.noutrefresh()
            #curses.doupdate()