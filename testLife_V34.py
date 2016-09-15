# import numpy as np
from tkinter import *
from tkinter import messagebox
import random
import sys
import csv
import ast

bornv = 3
stv1 = 2
stv2 = 3

eckmanon = False

def life_rules(stat,val):
    global bornv
    global stv1
    global stv2
##    if stat == 0 and val == 3:
##        return 1
##    if stat == 0 and val != 3:
##        return 0  
##    if stat == 1 and val < 2:
##        return 0
##    if stat == 1 and val > 3:
##        return 0
##    if stat == 1 and val >= 2 & val <= 3:
##        return 1
    if stat == 0 and val == bornv or stat == 1 and val == stv1 or stat == 1 and val == stv2:
        return 1
    else:
        return 0


# constants
##welcome_file = "startbild"
welcome_file = "cgol.csv"
##welcome_file = "startbild.csv"
welcome_text = ""
##welcome_text = "game of     life                                            push startand  start your life now"


surprisefiles = ["spidy.csv",
                 "frog.csv","xplosion.csv",
                 "soul.csv","zoo.csv","battle.csv",
                 "wussl.csv","doh.csv","love.csv",
                 "shootout.csv", "mini.csv",
                 "stairs.csv","ultistair.csv",
                 "shootgally.csv","shootgally2.csv",
                 "thaking.csv","aline.csv"]

optionmenufiles = ["buddhas.csv","gosper.csv","tools.csv",
                   "karo.csv", "dieHard.csv","acorn.csv",
                   "inf1.csv","sierpinski.csv", "sierpinski101.csv",
                   "giant.csv"]
nowtemplt = "init"
screenwidth = 600
screenhight = 600
boardcols = 60 # anzahl spalten
boardrows = 60 # anzahl zeilen
speed = 3 # 0 < speed > 11
gencount = 0

# spritsarten dmg, timeout col1 col2 safetime
clsdict = {1:(-1,3, "black","grey",10),
           2:(0,50, "blue", "blue",10),
           3:(-8,10,"red","white",10),
           4:(-1,50,"yellow","yellow",10)}

eckmanfeld = 40
eckmanspeed = 2


coldict = dict()
coldict[0] = "red"
coldict[1] = "white"
coldict[2] = "green"
coldict[3] = "yellow"
coldict[4] = "Goldenrod"



spritlist = list()
keylock = False
eckmintro = True
gameover = False

def lifecol(stat):
    return coldict[stat]


def get_cwrh():
    cw = int(screenwidth/test.get_wid())
    rh = int(screenhight/test.get_hig())
    return (cw,rh)
    
def symbolmaker(xpo,ypo):
##    cw = int(screenwidth/test.get_wid())
##    rw = int(screenhight/test.get_hig())
    cw = get_cwrh()[0]
    rw = get_cwrh()[1]
    pol = (xpo * cw,ypo * rw)
    pul = (xpo * cw, (ypo * rw) + rw)
    pur = ((xpo * cw) + cw, (ypo * rw) + rw)
    por = ((xpo * cw) + cw, ypo * rw)
    
    return [pol,pul,pur,por]

def click_process(pos):
##    cw = int(screenwidth/test.get_wid())
##    rw = int(screenhight/test.get_hig())
    cw = get_cwrh()[0]
    rw = get_cwrh()[1]
    if pos[0] <= (test.get_wid() * rw + rw) and pos[1] <= (test.get_hig() * cw + cw):
        cellx = int(pos[0]/cw)
        celly = int(pos[1]/rw)
        test.toggle_field(cellx,celly)

def sanistr(txstr):
    pointpos = txstr.find(".")
    if pointpos is not -1:
        txstr[:pointpos]
    return txstr
            
def writetofile(stuff,flnme = "soul"):
    if flnme is not "soul":
        flnme = sanistr(flnme)
    w = csv.writer(open(flnme + ".csv", "w"))
    for key, val in stuff.items():
        w.writerow([key, val])

def readfromfile(filename):
    newd = {}
    for key, val in csv.reader(open(filename)):
        keyastupl = ast.literal_eval(key)    
        newd[keyastupl] = ast.literal_eval(val)
    return newd

def randomtmplt():
    global nowtemplt
    nexttmplt = random.choice(surprisefiles)
    if nexttmplt == nowtemplt:
        return randomtmplt()
    else:
        nowtemplt = nexttmplt
        return nexttmplt

def letrf(foli):
    al = []
    rans = foli
    cls = (1,2,3,4)
    cz = 1
    for ra in rans:
        for j in range(ra[0],ra[1]):
            ttt = (cz,j)
            al.append(ttt)
        cz = cz + 1
    return al

def printtoboard(pritex):
    stbwid = 6
    stbhig = 6
    stc = 0
    for stab in pritex:
        stdi = readfromfile(stab + ".csv")
        coords = list(stdi.keys())
        for coord in coords:
##            print(coord)
            if coord[0] < stbwid and coord[1] < stbwid:
                cellx= (coord[0] + (stc)*stbwid) % (boardcols)
                celly= coord[1] + int((stc * stbwid )/ (boardcols )) * stbhig
                if cellx == 0 and celly == 0:
##                    print("x= %s, y= %s, val= %s " % (cellx,celly,stdi[(coord[0],coord[1])]))
                    pass
                test.set_field(cellx,celly,stdi[(coord[0],coord[1])])
        stc = (stc + 1)
        
class gol_board(object):
    def __init__(self, wid, hig, anf= "NA"):
        self.wid = wid
        self.hig = hig
        self.board = self.mke_board()
        self.anfbed = anf
        self.setanf = self.set_anfbed(self.anfbed)
        self.playapos = (0,0)
        self.playadirc = (0,0)
        self.playastat = 2
        self.playalife = 8
        self.playbpos = (1,1)
        self.playbdirc = (0,0)
        self.playbstat = 4
        self.playblife = 5

    def mke_board(self):
        global gencount
        gencount = 0
        board = dict()
        for x in range(self.wid):
            for y in range(self.hig):
                board[(x,y)] = gol_field(x,y,0)
        return board

    def set_anfbed(self,arg):
        if arg == "NA":
            pass
        if arg == "test":
            self.set_field(1,1,1)
            self.set_field(1,2,1)
            self.set_field(1,3,1)
        if arg == "rnd":
            for x in range(self.get_wid()):
                for y in range(self.get_hig()):
                    statlist = list(coldict.keys())
                    self.set_field(x,y,random.choice([0,1]))
            
    def get_nfields(self):
        # returns total number of fields
        wid * hig

    def get_hig(self):
        # returns height
        return self.hig

    def set_fieldze(self):
        for i in range(1,self.wid):
            for y in range(1,self.hig):
                self.board[i,y].set_stat(0)
        
    def get_wid(self):
        #returns width
        return self.wid

    def update_wid(self,nwd,nhg):
        (self.wid, self.hig) = (nwd,nhg)

    def __str__(self):
        for x in range(self.get_wid()):
            xrow = list()
            for y in range(self.get_hig()):
                xrow.append(self.get_fieldval(x,y))
            print ("%s \n" % xrow)
        return "Hoehe = %s, breite = %s" % (self.hig, self.wid)

    def get_field(self,x,y):
        return "Feld x= %s, y= %s: %s" % (x,y, self.board[(x,y)].get_stat())

    def get_fieldval(self,x,y):
##        print("x= %s, y= %s" % (x,y))
        return self.board[(x,y)].get_stat()       

    def set_field(self,x,y,arg):
        self.board[(x,y)].set_stat(arg)

    def toggle_field(self,x,y):
        self.board[(x,y)].change_stat()

    def get_nbsum(self,field_x,field_y):
        reichw = 1
        wid = self.get_wid()
        hig = self.get_hig()
        nbsum = 0
        for x in range(-reichw,reichw + 1 ,1):
            for y in range(-reichw,reichw + 1,1):
                if not(x == 0 and y == 0):
                    nbx = (field_x + x)% self.get_wid()
                    nby = (field_y + y)% self.get_hig()
##                    print("zentr = %s,%s, nbr = %s,%s,ofset = %s, fieldval = %s" % (field_x,field_y,nbx,nby,y,self.get_fieldval(nbx,nby)))
                    nbsum = nbsum + self.get_fieldval(nbx,nby)
                    
        return nbsum

    def get_nextgen(self):
        new = dict()
        for x in range(self.wid):
            for y in range(self.hig):
##                print("xcor = %s, ycord= %s, feld= %s, nbsum= %s" % (x,y,self.get_fieldval(x,y),self.get_nbsum(x,y)))
                newstat = life_rules(self.get_fieldval(x,y),self.get_nbsum(x,y))
                new[(x,y)] = gol_field(x,y,newstat)
        self.board = new
##        print(self)

    def draw(self,canvas):
        for item in self.board:
            self.board[item].draw(canvas)

    def get_board(self):
        return self.board

    def get_board_as_dict(self):
        t = dict()
##        print(self.board)
        for item in self.board:
            t[item] = self.board[item].get_stat()
        return t

    def set_board_from_dict(self,newdict):
        global boardcols
        global boardrows 
        nrw = int(max(newdict)[0] + 1)
        ncl = int(len(newdict) / nrw) 
        boardcols = ncl 
        boardrows = nrw
##        print("ncl= %s, nrw= %s" % (ncl,nrw))
        self.update_wid(ncl,nrw)
        self.board = self.mke_board()
        for x in range(self.get_wid()):
            for y in range(self.get_hig()):
                newstat = newdict[(x,y)]
                self.set_field(x,y,newstat)

    def set_playa(self,coords):
        self.playapos = coords

    def set_playb(self,coords):
        self.playbpos = coords

    def set_playastat(self, newstat):
        self.playastat = newstat

    def set_playbstat(self, newstat):
        self.playbstat = newstat

    def get_playastat(self):
        return self.playastat

    def get_playbstat(self):
        return self.playbstat

    def get_playa(self):
        return self.playapos

    def get_playb(self):
        return self.playbpos

    def set_dirca(self,newdircx, newdircy):
        self.playadirc =  (newdircx,newdircy)

    def set_dircb(self,newdircx, newdircy):
        self.playbdirc =  (newdircx,newdircy)

    def get_dirca(self):
        return self.playadirc

    def get_dircb(self):
        return self.playbdirc


    def move_playa(self):
        xpo = (self.get_playa()[0] + self.playadirc[0]) % (self.get_wid())
        ypo = (self.get_playa()[1] + self.playadirc[1]) % (self.get_hig())
        if self.board[xpo,ypo].get_stat() == 0:
            self.set_playa((xpo,ypo))
        else:
            pass

    def move_playb(self):
        xpo = (self.get_playb()[0] + self.playbdirc[0]) % (self.get_wid())
        ypo = (self.get_playb()[1] + self.playbdirc[1]) % (self.get_hig())
        if self.board[xpo,ypo].get_stat() == 0:
            self.set_playb((xpo,ypo))
        else:
            pass


    def draw_playa(self,canvas):
        xps = self.playapos[0]
        yps = self.playapos[1]
        canvas.create_rectangle(symbolmaker(xps,yps)[0],
                                symbolmaker(xps,yps)[2],
                                fill=lifecol(self.playastat))

    def draw_playb(self,canvas):
        xps = self.playbpos[0]
        yps = self.playbpos[1]
        canvas.create_rectangle(symbolmaker(xps,yps)[0],
                                symbolmaker(xps,yps)[2],
                                fill=lifecol(self.playbstat))

    def set_playalife(self,inc):
        self.playalife = self.playalife + inc

    def get_playalife(self):
        return self.playalife

    def set_playblife(self,inc):
        self.playblife = self.playblife + inc

    def get_playblife(self):
        return self.playblife

class gol_field(object):
    def __init__(self,x,y,stat):
        self.x= x
        self.y= y
        self.alive = stat

    def set_stat(self, arg):
        self.alive = arg

    def change_stat(self):
        if self.alive:
            self.alive = 0
        else:
            self.alive = 1

    def get_stat(self):
        return self.alive

    def draw(self,canvas):
        canvas.create_rectangle(symbolmaker(self.x,self.y)[0],symbolmaker(self.x,self.y)[2],fill=lifecol(self.get_stat()))

class player(object):
    def __init(self):
        self.playapos = (0,0)
        self.playadirc = (0,0)
        self.playastat = 2
        self.playalife = 8

    def set_playa(self,coords):
        self.playapos = coords

    def set_playastat(self, newstat):
        self.playastat = newstat

    def get_playastat(self):
        return self.playastat

    def get_playa(self):
        return self.playapos

    def set_dirca(self,newdircx, newdircy):
        self.playadirc =  (newdircx,newdircy)

    def get_dirca(self):
        return self.playadirc

    def move_playa(self,board):
        xpo = (self.get_playa()[0] + self.playadirc[0]) % (board.get_wid())
        ypo = (self.get_playa()[1] + self.playadirc[1]) % (board.get_hig())
        if board[xpo,ypo].get_stat() == 0:
            self.set_playa((xpo,ypo))
        else:
            pass

    def draw_playa(self,canvas):
        xps = self.playapos[0]
        yps = self.playapos[1]
        canvas.create_rectangle(symbolmaker(xps,yps)[0],
                                symbolmaker(xps,yps)[2],
                                fill=lifecol(self.playastat))

    def set_playalife(self,inc):
        self.playalife = self.playalife + inc

    def get_playalife(self):
        return self.playalife

class sprits(object):
    def __init__(self,cls,age,pos):
        self.cls = cls
        self.col = clsdict[cls][2]
        self.age = age
        self.x = pos[0]
        self.y = pos[1]
        self.dirc = (0,0)
        self.stat = 1
        self.locked = False
        self.locktime = 0
        self.safeofset = False
        self.safeofsettime = 0

    def draw(self, canvas):
        canvas.create_rectangle(symbolmaker(self.x,self.y)[0],
                                symbolmaker(self.x,self.y)[2],
                                fill=self.col)

    def movesprits(self):
        if random.choice([1,2,3,4]) == 4:
            rnddir = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
        else:
            rnddir = self.dirc
        newx = (self.x + rnddir[0]) % (boardcols)
        newy = (self.y + rnddir[1]) % (boardrows)
        if test.get_fieldval(newx,newy) == 1:
##            print(newx,newy)
##            self.movesprits()
            pass
        else:
            self.x = newx
            self.y = newy
            self.dirc = rnddir

    def get_dmg(self):
        return clsdict[self.cls][0]

    def get_pos(self):
        return (self.x,self.y)

    def set_col(self):
        self.col = clsdict[self.cls][3]

    def get_cls(self):
        return self.cls

    def set_cls(self, newcls):
        self.cls = newcls
        self.col = clsdict[self.cls][2]

    def set_timeout(self):
        if not self.locked:
            self.locked = TRUE
            self.locktime = self.age
            #print("lockt at %s" % self.locktime)
        else:
            pass

    def get_age(self):
        return self.age

    def get_lock(self):
        return self.locked

    def check(self):
        if self.locked:
            if self.locktime + clsdict[self.cls][1] < self.age:
                #print("lckt %s, dauer %s, age %s" % (self.locktime, clsdict[self.cls][1], self.age))
                self.locked = FALSE
        if self.safeofsettime + clsdict[self.cls][4] < self.age:
            self.safeofset = False

    def incage(self):
        self.age = self.age + 1

    def get_safeofset(self):
        return self.safeofset

    def set_safeofset(self):
        self.safeofsettime = self.age
        self.safeofset = True

class gun(object):
    def __init__(self, cls = 0):
        self.cls = cls
        self.ldet = TRUE
        self.fired = FALSE
        self.ammo = 1000
        self.bulltls = list()

    def get_bullts(self):
        return self.bulltls

    def get_cls(self):
        return self.cls

    def shoot(self,pos,dir):
        #print("shot at %s,%s in %s,%s" % (pos[0],pos[1],dir[0],dir[1]))
        self.bulltls.append(bullet(pos,dir))
        self.fired = TRUE

    def process_gun(self):
        if self.fired:
            for blt in self.bulltls:
                #print(blt.get_pos())
                blt.move_bullet()
                blt.inc_age()
                if blt.get_age() > blt.get_duration():
                    self.bulltls.remove(blt)
            if len(self.bulltls) == 0:
                self.fired = False


class bullet(object):
    def __init__(self, pos, dir, dmg = 1, duration = 10):
        self.posx = pos[0]
        self.posy = pos[1]
        self.dir = dir
        self.age = 0
        self.dmg = dmg
        self.duration = duration
        self.col = "Plum"

    def get_pos(self):
        return (self.posx, self.posy)

    def set_pos(self,newpos):
        self.posx = newpos[0]
        self.posy = newpos[1]

    def move_bullet(self):
        self.posx = self.posx + self.dir[0]
        self.posy = self.posy + self.dir[1]

    def inc_age(self):
        self.age = self.age + 1

    def get_age(self):
        return self.age

    def get_dmg(self):
        return self.dmg

    def get_duration(self):
        return self.duration

    def draw(self, canvas):
        canvas.create_rectangle(symbolmaker(self.posx,self.posy)[0],
                                symbolmaker(self.posx,self.posy)[2],
                                fill=self.col)

asgun = gun(cls= 0)
bsgun = gun(cls = 1)
gunlist = [asgun, bsgun]

def load(): # initializes game by creating board with gol_board
    global speed
    global timer
    global test
    speed = 3
    timer = 0
##    print("initialized")
    test = gol_board(boardcols,boardrows)
    test.set_board_from_dict(readfromfile(welcome_file))
    printtoboard(welcome_text)
    rulesfromstr("B3S23")

def process(): # runs game by calling get_nextgen
    global timer
    global speed
    global living
    global gencount
    timer = timer + 1
##    print(timer%speed == 0 and living)  
    if timer%speed == 0 and living:
        if eckmanon:
            if timer % 30 == 0:
        #if timer % (speed * 2) == 0:
                test.get_nextgen()
                gencount = gencount + 1
                gcountvar.set(gencount)
                timer = 1

        else:
            test.get_nextgen()
            gencount = gencount + 1
            gcountvar.set(gencount)



##        print(gencount)

        if eckmanon:
            test.move_playa()
            test.move_playb()
            processsprits()
            eckmanlivar.set("Playa A:" + str(test.get_playalife()) + "   |  " + "Playa B:" + str(test.get_playblife()))

def initsprits():
    global spritlist
    spritlist = list()
    for x in range(1,30):
        randx = random.choice(range(0,boardcols))
        randy = random.choice(range(0,boardrows))
        randtyp = random.choice([1,2,1,1])
        inage = 0

        spritlist.append(sprits(randtyp,inage,(randx,randy)))

def check_zstoss(spr):
    global test
    global gameover
    global spritlist

    if spr.get_pos() == test.get_playa():

        if spr.get_cls() == 1 and not spr.get_safeofset(): # effekt bei schwarz
            test.set_playalife(spr.get_dmg())
            spr.set_safeofset()
        if spr.get_cls() == 2 and not spr.get_safeofset(): # effekt bei blau
            spr.set_cls(4)
            spr.set_safeofset()
        ##            print(test.get_playalife())
        if spr.get_cls() == 4 and not spr.get_safeofset(): # effekt bei gelb
            spr.set_timeout()
            spr.set_safeofset()

        if test.get_playalife() <= 0: #effekt wenn playa a tot
            test.set_playastat(3)
            gameover = True
            toggl_pause()
            test.set_fieldze()
            if boardcols == 60:
                printtoboard("              you        lose")
            if boardcols == 40:
                printtoboard("              you    lose")

    if spr.get_pos() == test.get_playb():
        if spr.get_cls() == 2 and not spr.get_safeofset():
            #print("plB cls %S" % spr.get_cls())
            spr.set_timeout()
            
        if spr.get_cls() == 1 and not spr.get_safeofset():
        ##                print(spr.get_cls())
            spr.set_cls(2)
            spr.set_safeofset()
        ##   print(spr.get_cls())
        ##            print(test.get_playalife())
            
        if spr.get_cls() == 4 and not spr.get_safeofset():
            test.set_playblife(spr.get_dmg())
            spr.set_safeofset()

        if test.get_playblife() <= 0:
            test.set_playbstat(3)
            toggl_pause()
            gameover = True
            #test = gol_board(boardcols,boardrows)
            test.set_fieldze()
            if boardcols == 60:
                printtoboard("              you        lose")
            if boardcols == 40:
                printtoboard("              you    lose")

##    for gun in gunlist:
##        for blt in gun.get_bullts():
##            if spr.get_pos() == blt.get_pos():
##                if gun.get_cls() == 0:
##                    spr.set_timeout()
##                if gun.get_cls() == 1 and spr.get_cls == 4:
##                    test.toggle_field(spr.get_pos()[0],spr.get_pos()[1])
##                    spritlist.remove(spr)

    #check_guns(spr,gunlist)

def check_guns(spr, guns):
    global spritlist
    for gun in guns:
        #gun.process_gun()
        for blt in gun.get_bullts():
            if spr.get_pos() == blt.get_pos() and  spr in spritlist:
                if gun.get_cls() == 0 :
                    if spr.get_cls() == 4:
                        test.toggle_field(spr.get_pos()[0],spr.get_pos()[1])
                        spritlist.remove(spr)
                if gun.get_cls() == 1:
                    if spr.get_cls() == 4:
                        test.toggle_field(spr.get_pos()[0],spr.get_pos()[1])
                        spritlist.remove(spr)


def processsprits():
    global gameover
    for spr in spritlist[:]:
        if not spr.get_safeofset and spr in spritlist:
            check_zstoss(spr)
            check_guns(spr,gunlist)
        if not spr.get_lock() and spr in spritlist:
            spr.movesprits()
            if not spr.get_safeofset():
                check_zstoss(spr)
                check_guns(spr,gunlist)
        if spr in spritlist:
            spr.check()
            spr.incage()
            #check_guns(spr,gunlist)
    for gun in gunlist:
        gun.process_gun()

    if len(spritlist) == 0:
        gameover = True
        toggl_pause()
        test.set_fieldze()
        if boardcols == 60:
            printtoboard("              you        win")
        if boardcols == 40:
            printtoboard("              you    win")


                    
    



# gui controlls
#### mausi

lstfield = None
def click_callback(event):
    global lstfield
    cw = get_cwrh()[0]
    rw = get_cwrh()[1]  
    cellx = int(event.x/cw)
    celly = int(event.y/rw)
##    print("field to toggle x=%s, y=%s" % (cellx,celly))
    test.toggle_field(cellx,celly)
    lstfield = (cellx,celly)

def clickdrg_callback(event):
    global lstfield
##    print(event.x,event.y)
##    rw = int(screenwidth/test.get_wid())
##    cw = int(screenhight/test.get_wid())
    cw = get_cwrh()[0]
    rw = get_cwrh()[1]
    if event.x <= (test.get_wid() * rw + rw) and event.x >= 0 and event.y <= (test.get_hig() * cw + cw) and event.y >= 0:
        cellx = int(event.x/cw)
        celly = int(event.y/rw)
        if lstfield == (cellx,celly):
            pass
        else:
##        print("field to toggle x=%s, y=%s" % (cellx,celly))
            lstfield = (cellx,celly)
            test.toggle_field(cellx,celly)

#### keypresses
            
def keypress_event(keypres):
##    print(repr(keypres.char))
##    print(keypres.keysym)
    keyprasstr = repr(keypres.char)
    keyprassym = keypres.keysym
    for entry in keylist:      
        if entry == keyprasstr and not keyprasstr == "'a'" and not keyprasstr == "'s'" and not keyprasstr == "'d'" and not keyprasstr == "'w'":
            #print(keyprasstr)
            keylist[entry][0]()
        if entry == keyprassym or entry == keyprasstr and not keyprasstr == "'q'" and not keyprasstr == "' '" and not keyprasstr == "'p'" and not keyprasstr == "'r'" and not keylock:
            #print(entry)
            keylist[entry][0](keylist[entry][2])
            pass

def keyrelease_event(keyrels):
    pass
##    movepla((0,0))

def movepla(dircts):
##    print(dircts)
    test.set_dirca(dircts[0],dircts[1])
##    print(test.get_playa())
##    print(test.get_dirca())

def moveplb(dircts):
##    print(dircts)
    test.set_dircb(dircts[0],dircts[1])

# buttons
def toggl_pause():
    global living
    global keylock
    global eckmintro
    global eckmanon
    global gameover
    global spritlist

    if not eckmanon:
        if living:
            living = False
            pause_button.configure(text = "start")
        else:
            living = True
            pause_button.configure(text = "Pause Life")
    else:
        if living:
            living = False
            keylock = True
            pause_button.configure(text = "start")
        else:
            if eckmintro and not gameover:
                start_eckman()
##                living = True
                eckmintro = False
                pause_button.configure(text = "Pause")
            if not eckmintro and not gameover:
                living = True
                keylock = False
                pause_button.configure(text = "Pause")
            if not eckmintro and gameover:
                del spritlist[:]
                eckmanon = False
                gameover = False
                eckmintro = True
                playeckman()

def incrspeed():
    global speed
    incrmt = -1
    newspeed = speed + incrmt
    if newspeed > 1:
        speed = newspeed
    else:
        speedUp_button.configure(text = "-", command=incrspeed)
        speed = 1
    
def decrspeed():
    global speed
    incrmt = 1
    newspeed = speed + incrmt
    speed = newspeed
    if speed > 1:
        speedUp_button.configure(text = "schnella", command=incrspeed)

def exitlife():
    global living
    living = False
    if messagebox.askokcancel("Quit", "You want to end this life"):
        root.destroy()

def savelife():
    global living
    living = False
    writetofile(test.get_board_as_dict())

def savewithname():
    global living
    living = False
    if len(savewithname_input.get()) <= 0:
        messagebox.showwarning("doh","name ist zu kurz")
    else:
        writetofile(test.get_board_as_dict(),savewithname_input.get())
        savewithname_input.delete(0, END)
    pass

def resurectlife():
    global living
    living = False
    newdict = readfromfile("soul.csv")
    test.set_board_from_dict(newdict)

presetslist = {"newrandm_button": ("rnd","New random",60,60),
           "newempty_button": ( "NA","New empty",60,60),
           "newrandmsmall_button": ("rnd","New random small",20,20),
           "newemptysmall_button": ("NA","New emtpy small",20,20)}

def playeckman():
    global eckmanon
    global test
    global boardcols
    global boardrows
    global living
    global eckmti
    global eckmintro
    living = False
    boardcols = eckmanfeld
    boardrows = eckmanfeld
    if not eckmanon:
        eckmti = 0
        eckmanon = True
        test = gol_board(boardcols,boardrows)
        test.set_playa((8,8))
        test.set_playb((9,9))
        rulesfromstr("B1S12")
        sidebar.pack_forget()
        toolbar.pack_forget()
        eckman_button.configure(text="Stop eckMan")
        if boardcols == 60:
            printtoboard("this is      eckman            use         arrow   keys                survive")
        if boardcols == 40:
            printtoboard(" this    is   eckman")

    else:
        eckmanon = False
        eckman_button.configure(text="Play eckMan")
        canvas.pack_forget()
        toolbar.pack(side=TOP, fill=X)
        sidebar.pack(side=LEFT, fill=Y)
        canvas.pack(padx=6,pady=6)
        newrules()
        rulesfromstr("B" + str(bornv) + "S" + str(stv1) + str(stv2))
        newrules()
        eckmintro = True

def start_eckman():
    global test
    global living
    global speed
    speed = eckmanspeed
    playaposx = int(boardcols/2)
    playaposy = int(boardrows/2)
    playbposx = int(boardcols/2)-1
    playbposy = int(boardrows/2)-1
    test = gol_board(boardcols,boardrows)
    test.set_playa((playaposx,playaposy))
    test.set_playb((playbposx,playbposy))
    test.set_field(0,0,1)
    living = True
    initsprits()
    pass

def shoot_gunna():
    asgun.shoot(test.get_playa(), test.get_dirca())

def shoot_gunnb():
    bsgun.shoot(test.get_playb(), test.get_dircb())

def newrand():
    global living
    global test
    global timer
    global boardcols
    global boardrows
    boardrows = 60
    boardcols = 60
    if living:
        living = False
    test = gol_board(boardcols,boardrows,"rnd")
    timer = 0

def newempty():
    global living
    global test
    global timer
    global boardcols
    global boardrows
    boardrows = 60
    boardcols = 60
    if living:
        living = False
    test = gol_board(boardcols,boardrows,"NA")
    timer = 0
    
def newrandsmall():
    global living
    global test
    global boardcols
    global boardrows
    boardrows = 20
    boardcols = 20
    if living:
        living = False
    test = gol_board(boardcols,boardrows,"rnd")
    timer = 0

def newemptysmall():
    global living
    global test
    global boardcols
    global boardrows
    boardcols = 20
    boardrows = 20
    if living:
        living = False
    test = gol_board(boardcols,boardrows,"NA")
    timer = 0    
    
def newrandverysmall():
    global living
    global test
    global boardcols
    global boardrows
    boardcols = 8
    boardrows = 8
    if living:
        living = False
    test = gol_board(boardcols,boardrows,"rnd")
    timer = 0

def newemptyverysmall():
    global living
    global test
    global boardcols
    global boardrows
    boardcols = 8
    boardrows = 8
    if living:
        living = False
    test = gol_board(boardcols,boardrows,"NA")
    timer = 0    
    
def newtemplt():
    newdict = dict()
    global living
    living = False
    filenam = randomtmplt()
##    print(filenam)
    newdict = readfromfile(filenam)
    test.set_board_from_dict(newdict)
    rulesfromstr("B3S23")

def newfromwahl(tmplwahl):
    global living
    living = False
    newdict = readfromfile(tmplwahl)
    test.set_board_from_dict(newdict)
    if tmplwahl[:10] == "sierpinski":
        rulesfromstr("B1S12")
    else:
        rulesfromstr("B3S23")

def newrulestest(inptstr):
    if inptstr[0] == "B" and inptstr[2]=="S":
        return True
    else:
        return False

def newrules():
    global living
    living = False
    if len(rules_input.get()) == 5 and newrulestest(rules_input.get()):
        rulesfromstr(rules_input.get())
    else:
        messagebox.showwarning("oh no","Regeln in der Form: B3S23 (born wenn 3 Nachbarn, survive wenn 2 oder 3 Nachbarn)")
        rulesvar.set("B" + str(bornv) + "S" + str(stv1) + str(stv2))
##        savewithname_input.delete(0, END)

def rulesfromstr(rulestr):
    global bornv
    global stv1
    global stv2
    bornv = int(rulestr[1])
    stv1 = int(rulestr[3])
    stv2 = int(rulestr[4])
    rulesvar.set("B" + str(bornv) + "S" + str(stv1) + str(stv2))

def sierpin():
    global living
    global bornv
    global stv1
    global stv2
    global test
    global timer
    global boardcols
    global boardrows

    living = False
    boardrows = 100
    boardcols = 100
    rulesfromstr("B1S12")
    test = gol_board(boardcols,boardrows,"NA")
    timer = 0
    startx = int(boardcols/2)
    starty = int(boardrows/2)
    test.set_field(startx,starty,1)


keylist = {"' '":(toggl_pause,"Start/Stop"),
           "'q'":(exitlife,"exit"),
           "Up":(movepla,"up",(0,-1)),
           "Down":(movepla,"up",(0,1)),
           "Right":(movepla,"up",(1,0)),
           "Left":(movepla,"up",(-1,0)),
           "'w'":(moveplb,"up",(0,-1)),
           "'s'":(moveplb,"up",(0,1)),
           "'d'":(moveplb,"up",(1,0)),
           "'a'":(moveplb,"up",(-1,0)),
           "'p'":(shoot_gunna,"Ashoot"),
           "'r'":(shoot_gunnb,"Bshoot")}


templt_wahl_list = optionmenufiles


timer = 0
living = False

def draw():
    canvas.delete("all")
    test.draw(canvas)
    if eckmanon:
        test.draw_playa(canvas)
        test.draw_playb(canvas)
        for gun in gunlist:
            for blt in gun.get_bullts():
                blt.draw(canvas)
        for spr in spritlist:
            spr.draw(canvas)

##    pass

# process and draw the next frame
def frame():
    global living
    global speed
    if living:
        pass
    else:
        pause_button.configure(text = "start", command=toggl_pause)

    if speed == 1:
        speedUp_button.configure(text = "-", command=incrspeed)
        
    process()
    draw()
    root.after(50, frame)

# main loop

root = Tk()

mcol = "black"
tcol = "black"

# create a toolbar
buttonwid = 5
toolbar = Frame(root)
toolbar.configure(background=tcol)

toolbarmain = Frame(root)
toolbarmain.configure(background=tcol)

toolbareckman = Frame(root)
toolbareckman.configure(background=tcol)

eckmanlivar = StringVar()


pause_button = Button(toolbarmain, text="start", command=toggl_pause, width=buttonwid + 6)
pause_button.pack(side=LEFT, padx=17, pady=2)

eckmanstat_label = Label(toolbarmain,textvariable = eckmanlivar, width=20)
eckmanstat_label.pack(side=LEFT, padx=2, pady=2)


speedUp_button = Button(toolbar, text="schnella", command=incrspeed, width=buttonwid)
speedUp_button.pack(side=LEFT, padx=1, pady=2)

speedDown_button = Button(toolbar, text="langsama", command=decrspeed, width=buttonwid)
speedDown_button.pack(side=LEFT, padx=1, pady=2)

quit_button = Button(toolbarmain, text="Exit Life", command=exitlife, width=buttonwid)
quit_button.pack(side=RIGHT, padx=17, pady=2)

save_button = Button(toolbar, text="save Life", command=savelife, width=buttonwid)
save_button.pack(side=LEFT, padx=2, pady=2)

resurect_button = Button(toolbar, text="resurrect", command=resurectlife, width=buttonwid)
resurect_button.pack(side=LEFT, padx=2, pady=2)

savewithname_button = Button(toolbar, text="save as", command=savewithname, width=buttonwid)
savewithname_button.pack(side=RIGHT, padx=2, pady=2)

savewithname_input = Entry(toolbar, width= 8)
savewithname_input.pack(side=RIGHT, padx=2, pady=2)

eckman_button = Button(toolbarmain, text="play eckMan", command = playeckman, width=11)
eckman_button.pack(side=RIGHT, padx=2, pady=2)

toolbarmain.pack(side=TOP, fill=X)
toolbar.pack(side=TOP, fill=X)

# create a sidebar
sidebarwid = 40
sidebuttonwid =7
spcbut = 5
sidebar = Frame(root,width = sidebarwid)
sidebar.configure(background = tcol)
sidebarlabwi = 15

templtwahlvar = StringVar(sidebar)
templtwahlvar.set("-")

##newrandmverysmall_button = Button(sidebar, text="New random very small", command=newrandverysmall, width=sidebuttonwid, wraplength= sidebuttonwid * 8)
##newrandmverysmall_button.pack(side=BOTTOM, padx=2, pady=2)

##newsierpinski_button = Button(sidebar, text="Sierpinski", command=sierpin, width=sidebuttonwid, wraplength= sidebuttonwid * 8)
##newsierpinski_button.pack(side=BOTTOM, padx=2, pady=2)

newemptyverysmall_button = Button(sidebar, text="Neu leer ganz klein", command=newemptyverysmall, width=sidebuttonwid, wraplength= sidebuttonwid * 8)
newemptyverysmall_button.pack(side=BOTTOM, padx=2, pady=2)

##newrandmsmall_button = Button(sidebar, text="New random small", command=newrandsmall, width=sidebuttonwid, wraplength= sidebuttonwid * 8)
##newrandmsmall_button.pack(side=BOTTOM, padx=2, pady=2)

newemptysmall_button = Button(sidebar, text="neu leer klein", command=newemptysmall, width=sidebuttonwid, wraplength= sidebuttonwid * 8)
newemptysmall_button.pack(side=BOTTOM, padx=2, pady=2)

newrandm_button = Button(sidebar, text="neu chaos", command=newrand, width=sidebuttonwid, wraplength= sidebuttonwid * 8)
newrandm_button.pack(side=BOTTOM, padx=2, pady=2)

newempty_button = Button(sidebar, text="neu leer", command=newempty, width=sidebuttonwid, wraplength= sidebuttonwid * 8)
newempty_button.pack(side=BOTTOM, padx=2, pady=2)

templt_wahl = OptionMenu(sidebar, templtwahlvar, *templt_wahl_list, command = newfromwahl)
templt_wahl.pack(side=BOTTOM, padx=2, pady=2)
templt_wahl.config(width=spcbut)

newtemplt_button = Button(sidebar, text="zufall", command=newtemplt, width=sidebuttonwid, wraplength= sidebuttonwid * 8)
newtemplt_button.pack(side=BOTTOM, padx=2, pady=2)

##rulesvar = StringVar()
##rules_label = Label(sidebar, textvariable = rulesvar, width= sidebuttonwid)
##rules_label.pack(side=TOP, padx=2, pady=25)

tmpl_label = Label(sidebar, text="Startpos", width=sidebarlabwi)
tmpl_label.pack(side=BOTTOM, padx=2, pady=2)

rulesload_button = Button(sidebar, text="load", command=newrules, width=sidebuttonwid, wraplength= sidebuttonwid * 8)
rulesload_button.pack(side=BOTTOM, padx=2, pady=2)

rulesvar = StringVar()
rules_input = Entry(sidebar, width= int(sidebuttonwid), textvariable= rulesvar)
rules_input.pack(side=BOTTOM, padx=2, pady=2)

rules_label = Label(sidebar, text="Regeln", width=sidebarlabwi)
rules_label.pack(side=BOTTOM, padx=2, pady=2)

gencounttit_label = Label(sidebar, text="Generation", width= sidebarlabwi)
gencounttit_label.pack(side=TOP, padx=2, pady=2)

gcountvar = StringVar()
gencount_label = Label(sidebar, textvariable = gcountvar, width=5)
gencount_label.pack(side=TOP, padx=2, pady=2)


                       
sidebar.pack(side=LEFT, fill=Y)


root.title("testLife")
root.configure(background= mcol)
canvas = Canvas(root, width=screenwidth, height=screenhight, highlightthickness=0, bd=0, bg='black')
canvas.pack(padx=6,pady=6)
load()
frame()
canvas.bind("<Button-1>", click_callback)
canvas.bind("<B1-Motion>", clickdrg_callback)
root.bind("<Key>",keypress_event)
root.bind("<Any-KeyRelease>", keyrelease_event)
if "idlelib" not in sys.modules:
    root.mainloop()
