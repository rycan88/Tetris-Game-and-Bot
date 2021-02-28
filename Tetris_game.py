
import pygame,sys,time,math,os,random
from threading import Timer
class Square(object):
    S={} #List of Squares
    Stuck=set()
    def __init__(self,width,height,xpos,ypos):
        self.width=width-1
        self.height=height-1
        self.xpos=xpos
        self.ypos=ypos
        self.color=black
        self.xspd=0
        self.yspd=0
        x=(xpos-startcoords[0])//ss
        y=(ypos-startcoords[1])//ss
        Square.S[(x,y)]=self
        self.coord=(x,y)
    def redraw(self):
        pygame.draw.rect(screen,self.color,[self.xpos,self.ypos,self.width,self.height])
    def move(self,direction):
        global current
        newcoord=add(self.coord,direction)
        if newcoord in Square.S and newcoord not in Square.Stuck:
            Square.S[newcoord].color=self.color
            self.color = black
    def rotate(self,pivot,mode):
        coord=subtract(self.coord,pivot)
        if mode=="cw":
            addition=(-coord[1],coord[0])
        else:
            addition=(coord[1],-coord[0])
        newcoord=add(pivot,addition)
        if newcoord in Square.S and newcoord not in Square.Stuck:
            Square.S[newcoord].color = self.color
            self.color = black
    def moveable(self,direction):
        newcoord = add(self.coord, direction)
        if newcoord in Square.S and newcoord not in Square.Stuck:
            return newcoord
        return False
    def rotateable(self,pivot,mode):
        coord = subtract(self.coord, pivot)
        if mode=="cw":
            addition=(-coord[1],coord[0])
        else:
            addition=(coord[1],-coord[0])
        newcoord = add(pivot, addition)
        if newcoord in Square.S and newcoord not in Square.Stuck:
            return newcoord
        return False
    def removerow(self):
        row=self.coord[1]
        for x in range(10):
            Square.S[(x,row)].color=black
            Square.Stuck.remove((x,row))
        for y in range(row-1,-1,-1):
            for x in range(10):
                square=Square.S[(x,y)]
                newcoord = add((x,y), (0,1))
                Square.S[newcoord].color = square.color
                square.color = black
                if (x,y) in Square.Stuck:
                    Square.Stuck.remove((x,y))
                    Square.Stuck.add(newcoord)
    def remove(self):
        self.color=black

class Block(object):
    blue = (0, 0, 102)
    yellow = (255,204,0)
    purple = (102,0,102)
    orange = (255,102,0)
    green = (0,102,0)
    cyan = (0,143,179)
    red = (204,0,0)
    Shape=[(yellow,((1,1),(0,1),(0,0),(1,0)),(0.5,0.5)),(orange,((-1,1),(1,0),(0,0),(-1,0)),(0,0)),(blue,((1,1),(1,0),(0,0),(-1,0)),(0,0)),(red,((0,1),(1,1),(0,0),(-1,0)),(0,1)),(green,((0,1),(-1,1),(0,0),(1,0)),(0,1)),(cyan,((2,0),(1,0),(0,0),(-1,0)),(0.5,0.5)),(purple,((0,1),(1,0),(0,0),(-1,0)),(0,0))] #(color,coords relative,pivot)
    Next=[]
    def __init__(self,coord,shape=None):
        if shape==None:
            self.shape=random.randint(0,6)
        else:
            self.shape=shape
        self.Coords=[]
        self.coord=coord
        mode=Block.Shape[self.shape]

        self.color=mode[0]

        if mode[2]!=None:
            self.pivot=add(mode[2],coord)
        else:
            self.pivot=None
        for x in mode[1]:
            self.Coords.append(add(coord,x))
        for x in self.Coords:
            if x not in Square.S:
                self.remove()
                self.Coords=[]
                break
            Square.S[x].color = self.color
    def move(self,direction):
        global current,POINTS,interval,lag,ROWS,t,LEVEL
        running=self.moveable(direction)
        if running:
            for x in directionsort(self.Coords,direction):
                Square.S[x].move(direction)
            self.coord=add(self.coord,direction)
            for x in range(len(self.Coords)):
                self.Coords[x]=add(self.Coords[x],direction)
            if self.pivot!=None:
                self.pivot=add(self.pivot,direction)
            #RedrawBoard()
            return True
        else:
            if direction==(0,1):
                for x in directionsort(self.Coords,direction):
                    Square.Stuck.add(x)
                    if x[1]<0:
                        print("YOU LOSE")
                        print("LEVEL:",LEVEL)
                        print("ROWS:",ROWS)
                        print("POINTS:",POINTS)
                        print(Sequence)

                        time.sleep(5)
                        t.cancel()
                        sys.exit()
                counter = 0
                for y in range(20):
                    running = True
                    for x in range(10):
                        if (x, y) not in Square.Stuck:
                            running = False
                            break
                    if running:
                        counter += 1
                        Square.S[0,y].removerow()
                        ROWS+=1
                POINTS += LinePoints[counter]*(LEVEL+1)
                Sequence.append(current.shape)
                current=Block((4,-2),Block.Next[0].shape)
                Block.Next.pop(0)
                removeup()
                if len(OldSequence)>0:
                    Block.Next.append(Block((17,17),OldSequence.pop(0)))
                else:
                    prev = Block.Next[-1].Shape
                    colour = random.randint(0, 7)
                    if colour == prev or colour == 7:
                        Block.Next.append(Block((17, 17)))
                    else:
                        Block.Next.append(Block((17, 17), colour))


                if INITIAL_LEVEL>=18:
                    LEVEL = max(LEVEL,(ROWS+60)//10)
                else:
                    LEVEL = max(LEVEL,ROWS//10)
                while LevelInterval[0][0] < LEVEL:
                    LevelInterval.pop(0)
                interval = LevelInterval[0][1] / 60
                #if ROWS > 100:
                #    sys.exit()

        #RedrawBoard()
        return False

    def rotate(self,mode):
        global current
        if self.rotateable(mode):
            Old=self.Coords[:]
            for x in range(len(self.Coords)):
                coord = subtract(self.Coords[x], self.pivot)
                if mode == "cw":
                    addition = (-coord[1], coord[0])
                else:
                    addition = (coord[1], -coord[0])
                newcoord = add(self.pivot, addition)
                newcoord = (int(newcoord[0]),int(newcoord[1]))
                self.Coords[x] = newcoord
            for x in Old:
                Square.S[x].color=black
            for x in self.Coords:
                Square.S[x].color=self.color
        else:
            running=True
            if self.moveable((-1,0)):
                self.move((-1,0))
                if self.rotateable(mode):
                    self.rotate(mode)
                    running=False
                else:
                    self.move((1,0))
            if running and self.moveable((1,0)):
                self.move((1,0))
                if self.rotateable(mode):
                    self.rotate(mode)
                else:
                    self.move((-1,0))
        #RedrawBoard()
    def moveable(self,direction):
        for x in self.Coords:
            if Square.S[x].moveable(direction)==False:
                return False
        return True
    def rotateable(self,mode):
        for x in self.Coords:
            if Square.S[x].rotateable(self.pivot,mode) == False:
                return False
        return True
    def remove(self):
        for x in self.Coords:
            Square.Stuck.remove(x)
            Square.S[x].remove()
def removeup():
    for row in range(4):
        for x in range(15, 20):
            Square.S[(x, row)].color = black
    for block in Block.Next:
        for x in range(4):
            block.move((0, -1))
def add(t1,t2):
    return (t1[0]+t2[0],t1[1]+t2[1])
def subtract(t1,t2):
    return (t1[0]-t2[0],t1[1]-t2[1])
def RedrawBoard():
    screen.fill(white)
    for text,textRect in changescore():
        screen.blit(text, textRect)
    for square in Board:
        if square.coord[0]<0:
            continue
        square.redraw()
    for square in Board2:
        square.redraw()
    pygame.display.update()


def directionsort(List,direction):
    if direction==(-1,0):
        return sorted(List)
    elif direction==(1,0):
        return sorted(List,reverse=True)
    elif direction==(0,1):
        return sorted(List,key=lambda x: x[1],reverse=True)
    elif direction==(0,-1):
        return sorted(List, key=lambda x: x[1])


def Fall():
    global t,lag,STOP
    if current.moveable((0,1))!=True and lag == True:
        lag = False
        t=Timer(0.3,Fall)
        t.start()
        return
    if STOP == False:
        lag = True
        current.move((0,1))
        t=Timer(interval,Fall)
        t.start()
        RedrawBoard()
def changescore():
    TextBoxes = [] #text,textRect
    Box = ["Level: "+str(LEVEL),"Rows: "+str(ROWS),"Score: "+str(POINTS)]
    for x in range(3):
        GetText(Box[x],(150,25*x+300),TextBoxes)
    return TextBoxes
def GetText(string,coord,TextBoxes):
    text = f.render(string, True, blue)
    textRect = text.get_rect()
    textRect.center = coord
    TextBoxes.append((text,textRect))



#---------------------------------Player functions---------------------------------
def PlayerMove(direction):
    global POINTS,STOP
    if direction == (0,-1):
        return
    elif direction == (0,1):
        POINTS+=1
    STOP = True
    current.move(direction)
    STOP = False
    RedrawBoard()
def Rotate(thing="cw"):
    global STOP
    STOP = True
    current.rotate(thing)
    STOP = False
    RedrawBoard()
def Harddrop():
    global t,POINTS,STOP
    STOP = True
    t.cancel()

    while current.move((0,1)):
        POINTS+=2
        RedrawBoard()
    time.sleep(interval*2)
    t=Timer(interval,Fall)
    t.start()
    STOP = False

def GetCurrent():
    return current
def GetNext():
    return Block.Next.copy()
def GetStuckBoard():
    return Square.Stuck.copy()
def GetPoints(counter):
    return LinePoints[counter]*(LEVEL+1)
def Exit():
    global t
    t.cancel()
    print("YOU LOSE")
    print("LEVEL:", LEVEL)
    print("ROWS:", ROWS)
    print("POINTS:", POINTS)
    print(Sequence)
    sys.exit()
#---------------------------------Player functions------------------------------------
def main():
    global mode
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    PlayerMove((-1,0))
                if event.key == pygame.K_RIGHT:
                    PlayerMove((1,0))
                if event.key == pygame.K_DOWN:
                    PlayerMove((0,1))
                if event.key == pygame.K_z:
                    Rotate("ccw")
                if event.key == pygame.K_x or event.key == pygame.K_UP:
                    Rotate("cw")
                if event.key == pygame.K_p:
                    t.cancel()
                    a=True
                    while a:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_p:
                                    Fall()
                                    a=False
                                    break

                if event.key == pygame.K_SPACE:
                    Harddrop()
            RedrawBoard()

pygame.init()
width=1280
height=700
x = 0
y = 30
size=[width,height]
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
pygame.init()
screen=pygame.display.set_mode(size)
pygame.mouse.set_visible(1)
pygame.display.set_caption("TETRIS")

black=(0,0,0)
blue=(0,0,255)
white=(200,200,200)





ss=35 #square size
startcoords=(300,0)
endcoords=(650,700)
Board=[]
for y in range(startcoords[1]-5*ss,endcoords[1],ss):
    for x in range(startcoords[0],endcoords[0],ss):
        Board.append(Square(ss,ss,x,y))

startcoords2=(850,0)
endcoords2=(1025,700)
Board2=[]
for y in range(startcoords2[1],endcoords2[1],ss):
    for x in range(startcoords2[0],endcoords2[0],ss):
        Board2.append(Square(ss,ss,x,y))
repeated=False #TRUE MEANS REPEAT A BOARD, FALSE MEANS NOT
OldSequence=[]
Sequence=[]
if not repeated: #NORMAL
    current=Block((4,-2))
    prev = current.Shape
    for x in range(5):
        colour = random.randint(0,7)
        if colour == prev or colour == 7:
            Block.Next.append(Block((17,x*4+1)))
        else:
            Block.Next.append(Block((17,x*4+1),colour))
        prev = Block.Next[-1].Shape
else: #LETS YOU REPEAT A BOARD
    OldSequence = [6, 1, 6, 0, 4, 3, 5, 5, 4, 2, 5, 4, 2, 0, 5, 0, 0, 1, 6, 0, 6, 1, 6, 4, 2, 1, 0, 1, 5, 2, 2, 6, 5, 2, 0, 5, 6, 2, 1, 3, 1, 2, 5, 3, 2, 6, 5, 1, 1, 6, 2, 4, 1, 6, 1, 5, 6, 4, 1, 1, 0, 4, 6, 1, 0, 1, 5, 0, 2, 3, 5, 6, 5, 2, 3, 3, 6, 3, 2, 2, 5, 5, 4, 1, 5, 5, 0, 3, 5, 5, 1, 2, 6, 4, 0, 1, 5, 6, 6, 0, 1, 2, 4, 4, 1, 5, 5, 4, 4, 3, 1, 6, 1, 6, 0, 6, 2, 0, 5, 0, 2, 0, 2, 4, 0, 3, 6, 6, 4, 4, 6, 2, 4, 3, 3, 5, 6, 1, 0, 6, 4, 1, 6, 5, 2, 4, 5, 0, 1, 2, 1, 5, 5, 5, 4, 0, 4, 3, 3, 3, 2, 0, 2, 6, 4, 3, 2, 1, 6, 2, 2, 5, 0, 2, 1, 6, 0, 1, 4, 5, 5, 6, 0, 3, 3, 3, 2, 1, 0, 3, 6, 1, 5, 4, 5, 4, 2, 2, 0, 2, 3, 3, 3, 0, 4, 1, 4, 1, 6, 5, 6, 6, 3, 6, 2, 6, 4, 4, 5, 1, 0, 0, 3, 1, 0, 6, 4, 3, 4, 5, 3, 5, 0, 5, 5, 2, 4, 6, 3, 3, 6, 4, 4, 1, 4, 1, 6, 1, 1, 0, 3, 2, 0]
    OldSequence = [6, 1, 4, 1, 2, 6, 4, 0, 6, 4, 5, 5, 6, 1, 5, 3, 4, 3, 2, 5, 4, 4, 3, 3, 1, 5, 6, 0, 2, 4, 5, 4, 6, 1, 0, 4, 2, 1, 4, 3, 5, 6, 1, 0, 3, 2, 3, 1, 4, 1, 3, 1, 1, 5, 2, 2, 2, 3, 3, 1, 5, 6, 5, 0, 4, 6, 6, 5, 0, 5, 6, 5, 1, 3, 5, 4, 5, 3, 2, 5, 3, 4, 3, 3, 5, 2, 2, 4, 4, 3, 4, 1, 1, 2, 4, 5, 3, 1, 3, 2, 3, 1, 5, 3, 1, 0, 5, 3, 1, 5, 2, 5, 5, 2, 4, 4, 2, 4, 1, 1, 4, 0, 1, 3, 6, 1, 6, 5, 3, 6, 2, 2, 1, 3, 1, 3, 4, 1, 6, 6, 5, 4, 2, 0, 2, 3, 5, 4, 3, 3, 6, 2, 5, 2, 6, 2, 1, 4, 5, 3, 6, 3, 6, 5, 2, 3, 5, 4, 0, 2, 4, 4, 1, 2, 0, 1, 1, 2, 4, 4, 6, 3, 4, 3, 3, 0, 3, 1, 4, 6, 6, 5, 3, 3, 0]

    current=Block((4,-2),OldSequence.pop(0))
    for x in range(5):
        Block.Next.append(Block((17,x*4+1),OldSequence.pop(0)))

#218913,247
mode=False
POINTS=0
ROWS = 0
INITIAL_LEVEL = 18
LEVEL = INITIAL_LEVEL

lag=True
STOP = False
LinePoints = {0:0, 1:40, 2:100, 3:300, 4:1200}

LevelInterval = [(0,48),(1,43),(2,38),(3,33),(4,28),(5,23),(6,18),(7,13),(8,8),(9,6),(12,5),(15,4),(18,3),(28,2),(math.inf,1)]
while LevelInterval[0][0]<LEVEL:
    LevelInterval.pop(0)

interval = LevelInterval[0][1] / 60
f = pygame.font.Font("freesansbold.ttf", 20)

Fall()

if __name__ == "__main__":
    main()
