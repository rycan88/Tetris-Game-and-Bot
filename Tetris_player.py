import Tetris_game as Tetris
import time,random,math,sys


def Drop(column,block): #drop the block into the column
    n=column-block.coord[0]
    if n!=0:
        m=n/abs(n)
        for x in range(int(abs(n))):
            Tetris.PlayerMove((m,0))
    Tetris.Harddrop()

def add(t1,t2):
    return (t1[0]+t2[0],t1[1]+t2[1])
def subtract(t1,t2):
    return (t1[0]-t2[0],t1[1]-t2[1])

def Score(board): #gives the board a score. The lower the better
    total=0
    heights = []
    Emp = [1]*20 #empty
    C = [-1]*20 #counter
    Ex = [1]*20 #Extra
    for x in range(10):
        empty=1
        bad=False
        last = 20
        for y in range(19,-1,-1): #checks for holes to know whether to add lots of points or not (both horizontally and vertically)
            if (x,y) in board:
                last = y
                if bad:
                    total+=(empty**2)*150*(20-y)
                    empty=1
                    bad=False
                else:
                    total+=(20-y)*2
                if y<=9:
                    total += 100000000

                if Emp[y]>1:
                    Ex[y]*=Emp[y]
                    Emp[y]=1
                    C[y]+=1
            else:
                Emp[y]+=1
                if bad:
                    empty+=1
                else:
                    bad=True
        if (x,-1) in board:
            total = math.inf
        heights.append(last)
    heights.append(-100) #Lets there be a heights[-1] and heights[11] for side cases

    for y in range(20):
        total+=Ex[y]*C[y]

    counter = 0
    for x in range(0,10):
        first = heights[x]-heights[x-1]
        second = heights[x]-heights[x+1]
        if min(first,second) >= 3:
            counter+=1
    total+=(counter)**2*10000

    return total
def Rotate(Coords,pivot): #rotates ccw
    for x in range(len(Coords)):
        coord = subtract(Coords[x], pivot)
        addition = (coord[1], -coord[0])
        newcoord = tuple(map(int,add(pivot, addition)))
        Coords[x] = newcoord
    return Coords
def RemoveRow(row,Board):
    for x in range(10):
        Board.remove((x,row))
    for y in range(row-1,-1,-1):
        for x in range(10):
            if (x,y) in Board:
                Board.remove((x,y))
                Board.add(add((x,y),(0,1)))
def FakeDrop(column,shape,heights):
    coord = (column,-2)
    Coords = []
    for x in shape:
        new = add(coord, x)
        if new[0]<0 or new[0]>9:
            return False
        Coords.append(new)

    mini = math.inf
    for c in Coords:
        mini = min(heights[c[0]]-c[1],mini)

    for x in range(len(Coords)):
        Coords[x] = add(Coords[x],(0,mini-1))
    Coords.sort(key = lambda x: (x[1],x[0]))
    return Coords
def Decision(board, turn, answer, SHAPE, prev=""): #answer = (position,rotations)
    global lowest,position,rotations,reps,oldprev
    mode = Tetris.Block.Shape[SHAPE]
    shape=list(mode[1])
    pivot=mode[2]
    heights = FindHeights(board)
    for times in range(RotateTimes[SHAPE]):
        for x in range(0,10):
            Coords = FakeDrop(x,shape,heights)
            if Coords == False:
                continue
            newboard = board.copy()
            newboard.update(Coords)

            for zzz,b in Coords: #"zzz" is just a place holder. This loop removes rows incase a row has been completed
                running = True
                for a in range(10):
                    if (a, b) not in newboard:
                        running = False
                        break
                if running:
                    RemoveRow(b, newboard)

            reps += 1
            score=Score(newboard)
            if turn==1:
                if score<lowest:
                    lowest=score
                    oldprev = prev
                    position,rotations = answer
                elif score == lowest:
                    if prev < oldprev:
                        position,rotations = answer

            else:
                if answer=="":
                    Decision(newboard,turn+1,(x,times),Next[turn].shape,score)
                else:
                    Decision(newboard,turn+1,answer,Next[turn].shape,score)
        if times == RotateTimes[SHAPE]:
            break
        shape=Rotate(shape,pivot)
    return position,rotations
def FindHeights(board):
    heights = []
    for x in range(10):
        for y in range(20):
            if (x,y) in board:
                break
            y+=1
        heights.append(y)
    return heights
RotateTimes = [1,4,4,2,2,2,4]
current="NOTHING"
while True:
    for event in Tetris.pygame.event.get(): #THIS LETS ME ALT TAB WITHOUT THE PROGRAM CRASHING
        if event.type == Tetris.pygame.QUIT:
            Tetris.Exit()

    if Tetris.GetCurrent()==current: #THIS WAITS FOR A NEW BLOCK
        continue
    reps = 0
    board=Tetris.GetStuckBoard()
    current=Tetris.GetCurrent()
    Next=Tetris.GetNext()
    lowest=math.inf #lowest score
    oldprev = math.inf
    position="" # column to drop into
    rotations="" #number of times to rotate
    t1 = time.time()

    column,rotations=Decision(board.copy(), 0, "", current.shape)
    mode = Tetris.Block.Shape[0]
    shape=list(mode[1])
    print(reps, current.shape, Next[0].shape)
    print(time.time() - t1, "TOTAL")
    if Tetris.GetCurrent()!=current: #THIS WAITS FOR A NEW BLOCK
        print(time.time()-t1,reps,current.shape,Next[0].shape,"RAWR")
        continue
    for x in range(rotations):
        Tetris.Rotate("ccw")
    Drop(column,Tetris.GetCurrent())



'''RECORD (It stopped when I took my charger out of the computer to make it slower)
LEVEL: 1439
ROWS: 14339
POINTS: 456,134,180'''


#140065   12.728