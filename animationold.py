import torch
import pygame
import time
import random

def update(e1floor,e2floor,e1num,e2num,screen,paslist,e1d,e2d,e1status,e2status):
    screen.fill("black")
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    if e1d == True:
        c1 = (75,255,75)
    else:
        c1 = (175,175,175)
    if e2d == True:
        c2 = (75,255,75)
    else:
        c2 = (175,175,175)
    r1 = pygame.draw.rect(screen,c1,[(e1floor//7)*200,600-(e1floor%7)*100,50,100])
    r2 = pygame.draw.rect(screen,c2,[(e2floor//7)*200+50,600-(e2floor%7)*100,50,100])
    screen.blit(my_font.render(str(e1num), True, (0,0,0)),r1)
    screen.blit(my_font.render(str(e2num), True, (0,0,0)),r2)
    screen.blit(my_font.render(e1status+e2status,True,(255,255,255)),(500,500))
    x = 100
    y = 600
    i = 0
    for _ in range(5):
        for _ in range(7):
            try:
                screen.blit(my_font.render(str(paslist[i]), True, (255,255,255)),(x,y))
            except:
                pass
            i += 1
            y = y - 100
        x += 200
        y = 600
    pygame.display.flip()

def normalization(num):
    if num > 0:
        return 1
    else:
        return 0

def stop(ef,ep,es,fl):
    u = False
    d = False
    ep1 = []
    for i in ep:
        ep1.append(i[1])
    try:
        for i in fl[ef]:
            if i[1] < ef:
                d = True
            if i[1] > ef:
                u = True
        if ef in ep1 or (es != 'down' and u == True) or (es != 'up' and d == True):
            return True
        else:
            return False
    except:
        print(ef,ep,es,fl)
        assert False

def simulate(model,passengerlist,floornum):

    #####REMOVE
    # inoutlist = []



    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    clock = pygame.time.Clock()
    running = True

    #list of passenger events
    passengerlist.sort(key = lambda x: x[0])
    #index of passenger events
    k = 0
    #list of floor passenger target floors
    floorlist = []
    for _ in range(floornum):
        floorlist.append([])

    #floor e1 is on
    elevator1 = 0
    #passenger data of e1
    elevator1p = []
    #door data of e1
    elevator1d = False
    #floor e2 is on
    elevator2 = 0
    #passenger data of e2
    elevator2p = []
    #door data of e2
    elevator2d = False

    #list of button presses upward
    buttonlistup = [0].copy()*floornum
    #list of button presses downward
    buttonlistdown = [0].copy()*floornum
    e1status = 'neutral'
    e2status = 'neutral'
    e1stoptime = 0
    e2stoptime = 0
    e1buttonlist = [0].copy()*floornum
    e2buttonlist = [0].copy()*floornum
    e1move = False
    e2move = False
    e1dir = 'n'
    e2dir = 'n'
    points = 0
    satisfaction = 0
    #simulation loop
    for t in range(1800):
        # tr = time.time()
        #adding passengers
        # print(passengerlist[k])
        try:
            while passengerlist[k][0] == t:
                floorlist[passengerlist[k][1]].append((passengerlist[k][0],passengerlist[k][2]))
                # print('attempted to add passenger')
                if passengerlist[k][1] < passengerlist[k][2]:
                    buttonlistup[passengerlist[k][1]] = 1
                else:
                    buttonlistdown[passengerlist[k][1]] = 1
                k += 1
        except:
            pass
            # print('error')

        if e1status == 'neutral':
            e1dir = 'n'
            if stop(elevator1,elevator1p,e1status,floorlist):
                elevator1d = True
                e1stoptime = 5
            else:
                e1stoptime = 0
                elevator1d = False
                e1move = False
                e1status = 'neutral'
        #elevator stopping
        if elevator1d == True:
            print('door open1')
            e1buttonlist[elevator1] = 0
            if len(elevator1p) == 0:
                e1status = 'neutral'
                e1stoptime = 0
            e1p1 = []
            for i in elevator1p:
                e1p1.append(i[1])
            if e1p1.count(elevator1) != 0:
                for element in elevator1p:
                    if element[1] == elevator1:
                        timetaken = t - element[0]
                        if timetaken <= 300:
                            points += 5
                        elif timetaken <= 600:
                            points += 9 - timetaken*0.0133
                        else:
                            points += 1
                    e1stoptime = 5
                for i in elevator1p:
                    if i[1] == elevator1:
                        elevator1p.remove(i)
            for passenger in floorlist[elevator1]:
                if e1status != 'down':
                    print('passenger boarded for up1')
                    if passenger[1] > elevator1 and len(elevator1p) < 15:
                        e1status = 'up'
                        # print('passenger in e1 up')
                        floorlist[elevator1].remove(passenger)
                        elevator1p.append(passenger)
                        buttonlistup[elevator1] = 0
                        e1stoptime = 5
                if e1status != 'up':
                    print('passenger boarded for down1')
                    if passenger[1] < elevator1 and len(elevator1p) < 15:
                        e1status = 'down'
                        # print('passenger in e1 down')
                        floorlist[elevator1].remove(passenger)
                        elevator1p.append(passenger)
                        buttonlistdown[elevator1] = 0
                        e1stoptime = 5
                e1buttonlist[passenger[1]] = 1

        if e2status == 'neutral':
            e2dir = 'n'
            if stop(elevator2,elevator2p,e2status,floorlist):
                elevator2d = True
                e2stoptime = 5
            else:
                e2stoptime = 0
                e2move = False
                elevator2d = False
                e2status = 'neutral'
        if elevator2d == True:
            print('door open2')
            e2buttonlist[elevator2] = 0
            if len(elevator2p) == 0:
                e2status = 'neutral'
                e2stoptime = -1
            e2p1 = []
            for i in elevator2p:
                e2p1.append(i[1])
            if e2p1.count(elevator2) != 0:
                for element in elevator2p:
                    if element[1] == elevator2:
                        timetaken = t - element[0]
                        if timetaken <= 300:
                            points += 5
                        elif timetaken <= 600:
                            points += 9 - timetaken*0.0133
                        else:
                            points += 1
                    e2stoptime = 5
                for i in elevator2p:
                    if i[1] == elevator2:
                        elevator2p.remove(i)
            for passenger in floorlist[elevator2]:
                if e2status != 'down':
                    if passenger[1] > elevator2 and len(elevator2p) < 15:
                        print('passenger boarded for up2')
                        # print('passenger in e2 up')
                        e2status = 'up'
                        floorlist[elevator2].remove(passenger)
                        elevator2p.append(passenger)
                        buttonlistup[elevator2] = 0
                        e2stoptime = 5
                if e2status != 'up':
                    if passenger[1] < elevator2 and len(elevator2p) < 15:
                        e2status = 'down'
                        print('passenger boarded for down2')
                        # print('passenger in e2 down')
                        floorlist[elevator2].remove(passenger)
                        elevator2p.append(passenger)
                        buttonlistdown[elevator2] = 0
                        e2stoptime = 5
                e2buttonlist[passenger[1]] = 1
        if e1stoptime > 0:
            e1stoptime = e1stoptime - 1
            if e1stoptime == 0:
                elevator1d = False
                e1move = False
        if e2stoptime > 0:
            e2stoptime = e2stoptime - 1
            if e2stoptime == 0:
                e2move = False
                elevator2d = False

        inputlist = [0].copy()*floornum*2
        inputlist[elevator1] = 1
        inputlist[elevator2+floornum] = 1
        inputlist.extend(buttonlistup)
        inputlist.extend(buttonlistdown)
        inputlist.extend(e1buttonlist)
        inputlist.extend(e2buttonlist)
        match e1status:
            case 'up':
                e1statusint = 1
            case 'neutral':
                e1statusint = 0
            case 'down':
                e1statusint = -1
        match e2status:
            case 'up':
                e2statusint = 1
            case 'neutral':
                e2statusint = 0
            case 'down':
                e2statusint = -1
        match elevator1d:
            case True:
                e1dint = 1
            case False:
                e1dint = 0
        match elevator2d:
            case True:
                e2dint = 1
            case False:
                e2dint = 0
        match e1dir:
            case 'up':
                e1dirint = 1
            case 'down':
                e1dirint = -1
            case 'n':
                e1dirint = 0
        match e2dir:
            case 'up':
                e2dirint = 1
            case 'down':
                e2dirint = -1
            case 'n':
                e2dirint = 0
    
        inputlist.extend([e1statusint,e2statusint,e1dint,e2dint,e1dirint,e2dirint])
        '''
        more things i need to put into input list:
        elevator door open close
        real elevator direction
        also make the network decide on open and closing doors 
        the idea is
        the doors will open only if people want to get on and off
        otherwise the door stays shut
        remember to test this new feature manually
        if the training fails:
            try to add like the next stop for the elevator for passengers inside, next stop for up, next stop for down
        '''
        inputs = torch.Tensor(inputlist)
        # print(time.time()-tr)
        logit = model(inputs)
        # logits = [0]*8
        # out = tradalg(inputlist)
        # print(elevator1p,elevator2p)
        # match out[0]:
        #     case 'u':
        #         logits[0] = 1
        #         logits[1] = 0
        #         logits[2] = 1
        #         logits[6] = 0
        #     case 'u1':
        #         logits[0] = 1
        #         logits[1] = 0
        #         logits[2] = 1
        #         logits[6] = 1
        #     case 'd':
        #         logits[0] = 0
        #         logits[1] = 1
        #         logits[2] = -1
        #         logits[6] = 0
        #     case 'd1':
        #         logits[0] = 0
        #         logits[1] = 1
        #         logits[2] = -1
        #         logits[6] = 1
        #     case 'n':
        #         logits[0] = 0
        #         logits[1] = 0
        #         logits[2] = 0
        #         logits[6] = 0
        # match out[1]:
        #     case 'u':
        #         logits[3] = 1
        #         logits[4] = 0
        #         logits[5] = 1
        #         logits[7] = 0
        #     case 'u1':
        #         logits[3] = 1
        #         logits[4] = 0
        #         logits[5] = 1
        #         logits[7] = 1
        #     case 'd':
        #         logits[3] = 0
        #         logits[4] = 1
        #         logits[5] = -1
        #         logits[7] = 0
        #     case 'd1':
        #         logits[3] = 0
        #         logits[4] = 1
        #         logits[5] = -1
        #         logits[7] = 1
        #     case 'n':
        #         logits[3] = 0
        #         logits[4] = 0
        #         logits[5] = 0
        #         logits[7] = 0
        update(elevator1,elevator2,len(elevator1p),len(elevator2p),screen,floorlist,elevator1d,elevator2d,e1status,e2status)
        # logits = list(map(int,input('list').split(' ')))
        # tr = time.time()
        # outputs: [e11,e12,up=1 down=0]
        # logits = torch.Tensor(logits)


        #####REMOVE
        # inoutlist.append((inputs.tolist(),logits.tolist()))

        # logits = logits.tolist()
        logit = logit.tolist()

        outputs = []
        for e in logit:
            outputs.append(normalization(e))
        if elevator1d == False:
            if e1move == False:
                # print('init')
                match (outputs[0],outputs[1]):
                    case (0,0):
                        pass
                        # print('stay neutral')
                    case (1,1):
                        pass
                        # print('stay neutral')
                    case (0,1):
                        # if t == 5:
                        #     points += 10
                        if outputs[6] == 0:
                            # print('going down')
                            elevator1 = elevator1 - 1
                            if elevator1 == -1:
                                # print('bottom floor. try again')
                                elevator1 = 0
                            else:
                                e1move = True
                                e1dir = 'down'
                                if elevator1 < 1:
                                    elevator1 = 0
                                    # print('reached bottom floor')
                                    e1status = 'up'
                                    e1dir = 'n'
                                    if stop(elevator1,elevator1p,e1status,floorlist):
                                        elevator1d = True
                                        e1stoptime = 5
                                    else:
                                        e1stoptime = 0
                                        e1status = 'neutral'
                                        e1move = False
                                        elevator1d = False
                        else:
                            # print('move down 1 floor')
                            # e1move = True
                            # if t == 6:
                            #     points += 10
                            elevator1 = elevator1 - 1
                            if elevator1 == -1:
                                elevator1 = 0
                                # print('reached bottom floor, try again')
                            if elevator1 == floornum-1:
                                e1status = 'up'
                            elif elevator1 == 0:
                                e1status = 'down'
                            elif outputs[2] == 1:
                                e1status = 'up'
                            else:
                                e1status = 'down'
                            e1dir = 'n'
                            if stop(elevator1,elevator1p,e1status,floorlist):
                                elevator1d = True
                                e1stoptime = 5
                            else:
                                e1stoptime = 0
                                e1status = 'neutral'
                                e1move = False
                                elevator1d = False
                            if outputs[2] == -1 and elevator1 > 0:
                                e1status == 'down'
                            else:
                                e1status == 'up'
                                
                    case (1,0):
                        if t == 11:
                            # points += 5
                            pass
                        if outputs[6] == 1:
                            # print('move up 1 floor')
                            # e1move = True
                            elevator1 = elevator1 + 1
                            if elevator1 == floornum:
                                elevator1 = floornum-1
                                # print('reached top floor, try again')
                            if elevator1 == floornum-1:
                                e1status = 'up'
                            elif elevator1 == 0:
                                e1status = 'down'
                            elif outputs[2] == 1:
                                e1status = 'up'
                            else:
                                e1status = 'down'
                            e1dir = 'n'
                            if stop(elevator1,elevator1p,e1status,floorlist):
                                elevator1d = True
                                e1stoptime = 5
                            else:
                                e1stoptime = 0
                                e1status = 'neutral'
                                e1move = False
                                elevator1d = False
                            if outputs[2] == 1 and elevator1 < floornum-1:
                                e1status == 'up'
                            else:
                                e1status == 'down'
                        else:
                            # print('going up')
                            elevator1 = elevator1 + 1
                            if elevator1 == floornum:
                                # print('top floor. try again')
                                elevator1 = floornum-1
                            else:
                                e1move = True
                                e1dir = 'up'
                                if elevator1 > floornum-2:
                                    elevator1 = floornum-1
                                    # print('reached top floor')
                                    e1status = 'down'
                                    e1dir = 'n'
                                    if stop(elevator1,elevator1p,e1status,floorlist):
                                        elevator1d = True
                                        e1stoptime = 5
                                    else:
                                        e1stoptime = 0
                                        e1move = False
                                        e1status = 'neutral'
                                        elevator1d = False
            else:
                # print('no init')
                match (outputs[0],outputs[1]):
                    case (0,0):
                        # if t == 6:
                        #     points += 10
                        # print('stopping elevator')
                        if e1dir == 'up':
                            elevator1 = elevator1 + 1
                        else:
                            elevator1 = elevator1 - 1
                        if elevator1 == floornum-1:
                            e1status = 'up'
                        elif elevator1 == 0:
                            e1status = 'down'
                        elif outputs[2] == 1:
                            e1status = 'up'
                        else:
                            e1status = 'down'
                        # there is no check here. if check implemented and activated, there was a problem with checking previous actions.
                        e1dir = 'n'
                        if stop(elevator1,elevator1p,e1status,floorlist):
                            elevator1d = True
                            e1stoptime = 5
                        else:
                            e1stoptime = 0
                            e1move = False
                            e1status = 'neutral'
                            elevator1d = False
                    case(1,1):
                        # if t == 6:
                        #     points += 10
                        # print('stopping elevator')
                        if e1dir == 'up':
                            elevator1 = elevator1 + 1
                        else:
                            elevator1 = elevator1 - 1
                        if elevator1 == floornum-1:
                            e1status = 'up'
                        elif elevator1 == 0:
                            e1status = 'down'
                        elif outputs[2] == 1:
                            e1status = 'up'
                        else:
                            e1status = 'down'
                        e1dir = 'n'
                        if stop(elevator1,elevator1p,e1status,floorlist):
                            elevator1d = True
                            e1stoptime = 5
                        else:
                            e1stoptime = 0
                            e1move = False
                            e1status = 'neutral'
                            elevator1d = False
                    case(1,0):
                        if outputs[6] == 1:
                            if e1dir == 'up':
                                elevator1 = elevator1 + 1
                            else:
                                elevator1 = elevator1 - 1
                            if elevator1 == floornum-1:
                                e1status = 'up'
                            elif elevator1 == 0:
                                e1status = 'down'
                            elif outputs[2] == 1:
                                e1status = 'up'
                            else:
                                e1status = 'down'
                            # there is no check here. if check implemented and activated, there was a problem with checking previous actions.
                            e1dir = 'n'
                            if stop(elevator1,elevator1p,e1status,floorlist):
                                elevator1d = True
                                e1stoptime = 5
                            else:
                                e1stoptime = 0
                                e1move = False
                                e1status = 'neutral'
                                elevator1d = False
                        else:
                            if e1dir == 'up':
                                # print('going up')
                                elevator1 = elevator1 + 1
                                if elevator1 > floornum-2:
                                    elevator1 = floornum-1
                                    # print('reached top floor')
                                    e1status = 'down'
                                    e1dir = 'n'
                                    if stop(elevator1,elevator1p,e1status,floorlist):
                                        elevator1d = True
                                        e1stoptime = 5
                                    else:
                                        e1stoptime = 0
                                        e1move = False
                                        e1status = 'neutral'
                                        elevator1d = False
                            else:
                                # print('wrong direction! stopping elevator')
                                elevator1 = elevator1 - 1
                                e1status = 'up'
                                #there is no check here. same as prev.
                                e1dir = 'n'
                                if stop(elevator1,elevator1p,e1status,floorlist):
                                    elevator1d = True
                                    e1stoptime = 5
                                else:
                                    e1stoptime = 0
                                    e1move = False
                                    e1status = 'neutral'
                                    elevator1d = False

                    case (0,1):
                        if outputs[6] == 1:
                            if e1dir == 'up':
                                elevator1 = elevator1 + 1
                            else:
                                elevator1 = elevator1 - 1
                            if elevator1 == floornum-1:
                                e1status = 'up'
                            elif elevator1 == 0:
                                e1status = 'down'
                            elif outputs[2] == 1:
                                e1status = 'up'
                            else:
                                e1status = 'down'
                            # there is no check here. if check implemented and activated, there was a problem with checking previous actions.
                            e1dir = 'n'
                            if stop(elevator1,elevator1p,e1status,floorlist):
                                elevator1d = True
                                e1stoptime = 5
                            else:
                                e1stoptime = 0
                                e1move = False
                                e1status = 'neutral'
                                elevator1d = False
                        else:
                            if e1dir == 'down':
                                elevator1 = elevator1 - 1
                                # print('going down')
                                if elevator1 < 1:
                                    elevator1 = 0
                                    # print('reached bottom floor')
                                    e1status = 'up'
                                    e1dir = 'n'
                                    if stop(elevator1,elevator1p,e1status,floorlist):
                                        elevator1d = True
                                        e1stoptime = 5
                                    else:
                                        e1stoptime = 0
                                        e1move = False
                                        e1status = 'neutral'
                                        elevator1d = False
                            else:
                                # print('wrong direction! stopping elevator')
                                elevator1 = elevator1 + 1
                                e1status = 'down'
                                #there is no check here. same as prev.
                                e1dir = 'n'
                                if stop(elevator1,elevator1p,e1status,floorlist):
                                    elevator1d = True
                                    e1stoptime = 5
                                else:
                                    e1stoptime = 0
                                    e1move = False
                                    e1status = 'neutral'
                                    elevator1d = False

        if elevator2d == False:
            if e2move == False:
                # print('e2init')
                match (outputs[3],outputs[4]):
                    case (0,0):
                        pass
                        # print('neutral e2')
                    case (1,1):
                        pass
                        # print('neutral e2')
                    case (0,1):
                        if outputs[7] == 0:
                            # print('going down')
                            elevator2 = elevator2 - 1
                            if elevator2 == -1:
                                # print('bottom floor. try again')
                                elevator2 = 0
                            else:
                                e2move = True
                                e2dir = 'down'
                                if elevator2 < 1:
                                    elevator2 = 0
                                    # print('reached bottom floor')
                                    e2status = 'up'
                                    e2dir = 'n'
                                    if stop(elevator2,elevator2p,e2status,floorlist):
                                        elevator2d = True
                                        e2stoptime = 5
                                    else:
                                        e2stoptime = 0
                                        e2move = False
                                        e2status = 'neutral'
                                        elevator2d = False
                        else:
                            # print('move down 1 floor')
                            # e2move = True
                            elevator2 = elevator2 - 1
                            if elevator2 == -1:
                                elevator2 = 0
                                # print('reached bottom floor, try again')
                            if elevator1 == floornum-1:
                                e1status = 'up'
                            elif elevator1 == 0:
                                e1status = 'down'
                            elif outputs[2] == 1:
                                e1status = 'up'
                            else:
                                e1status = 'down'
                            e2dir = 'n'
                            if stop(elevator2,elevator2p,e2status,floorlist):
                                elevator2d = True
                                e2stoptime = 5
                            else:
                                e2stoptime = 0
                                e2move = False
                                elevator2d = False
                                e2status = 'neutral'
                            if outputs[5] == -1 and elevator2 > 0:
                                e2status == 'down'
                            else:
                                e2status == 'up'
                    case (1,0):
                        if outputs[7] == 0:
                            # print('going up')
                            elevator2 = elevator2 + 1
                            if elevator2 == floornum:
                                # print('top floor. try again')
                                elevator2 = floornum-1
                            else:
                                e2move = True
                                e2dir = 'up'
                                if elevator2 > floornum-2:
                                    elevator2 = floornum-1
                                    # print('reached top floor')
                                    e2status = 'down'
                                    e2dir = 'n'
                                    if stop(elevator2,elevator2p,e2status,floorlist):
                                        elevator2d = True
                                        e2stoptime = 5
                                    else:
                                        e2stoptime = 0
                                        e2move = False
                                        elevator2d = False
                                        e2status = 'neutral'
                        else:
                            # print('move up 1 floor')
                            # e2move = True
                            elevator2 = elevator2 + 1
                            if elevator2 == floornum:
                                elevator2 = floornum-1
                                # print('reached top, try again')
                            if elevator1 == floornum-1:
                                e1status = 'up'
                            elif elevator1 == 0:
                                e1status = 'down'
                            elif outputs[2] == 1:
                                e1status = 'up'
                            else:
                                e1status = 'down'
                            e2dir = 'n'
                            if stop(elevator2,elevator2p,e2status,floorlist):
                                elevator2d = True
                                e2stoptime = 5
                            else:
                                e2stoptime = 0
                                e2move = False
                                elevator2d = False
                                e2status = 'neutral'
                            if outputs[5] == 1 and elevator2 < floornum-1:
                                e2status == 'up'
                            else:
                                e2status == 'down'
            else:
                # print('no e2init')
                match (outputs[3],outputs[4]):
                    case (0,0):
                        # print('stopping elevator')
                        if e2dir == 'up':
                            elevator2 = elevator2 + 1
                        else:
                            elevator2 = elevator2 - 1
                        if elevator2 == floornum-1:
                            e2status = 'up'
                        elif elevator2 == 0:
                            e2status = 'down'
                        elif outputs[5] == 1:
                            e2status = 'up'
                        else:
                            e2status = 'down'
                        #no check here. same
                        e2dir = 'n'
                        if stop(elevator2,elevator2p,e2status,floorlist):
                            elevator2d = True
                            e2stoptime = 5
                        else:
                            e2stoptime = 0
                            e2move = False
                            elevator2d = False
                            e2status = 'neutral'
                    case(1,1):
                        # print('stopping elevator')
                        if e2dir == 'up':
                            elevator2 = elevator2 + 1
                        else:
                            elevator2 = elevator2 - 1
                        if elevator2 == floornum-1:
                            e2status = 'up'
                        elif elevator2 == 0:
                            e2status = 'down'
                        elif outputs[5] == 1:
                            e2status = 'up'
                        else:
                            e2status = 'down'
                        #no check
                        e2dir = 'n'
                        if stop(elevator2,elevator2p,e2status,floorlist):
                            elevator2d = True
                            e2stoptime = 5
                        else:
                            e2stoptime = 0
                            e2move = False
                            elevator2d = False
                            e2status = 'neutral'
                    case(1,0):
                        if outputs[7] == 1:
                            if e2dir == 'up':
                                elevator2 = elevator2 + 1
                            else:
                                elevator2 = elevator2 - 1
                            if elevator2 == floornum-1:
                                e2status = 'up'
                            elif elevator2 == 0:
                                e2status = 'down'
                            elif outputs[5] == 1:
                                e2status = 'up'
                            else:
                                e2status = 'down'
                            #no check here. same
                            e2dir = 'n'
                            if stop(elevator2,elevator2p,e2status,floorlist):
                                elevator2d = True
                                e2stoptime = 5
                            else:
                                e2stoptime = 0
                                e2move = False
                                elevator2d = False
                                e2status = 'neutral'
                        else:
                            if e2dir == 'up':
                                # print('going up')
                                elevator2 = elevator2 + 1
                                if elevator2 > floornum-2:
                                    elevator2 = floornum-1
                                    # print('reached top floor')
                                    e2status = 'down'
                                    e2dir = 'n'
                                    if stop(elevator2,elevator2p,e2status,floorlist):
                                        elevator2d = True
                                        e2stoptime = 5
                                    else:
                                        e2stoptime = 0
                                        e2move = False
                                        elevator2d = False
                                        e2status = 'neutral'
                            else:
                                # print('wrong direction! stopping elevator')
                                e2dir = 'up'
                                elevator2 = elevator2 - 1
                                #no
                                e2dir = 'n'
                                if stop(elevator2,elevator2p,e2status,floorlist):
                                    elevator2d = True
                                    e2stoptime = 5
                                else:
                                    e2stoptime = 0
                                    e2move = False
                                    e2status = 'neutral'
                                    elevator2d = False
                    case (0,1):
                        if outputs[7] == 1:
                            if e2dir == 'up':
                                elevator2 = elevator2 + 1
                            else:
                                elevator2 = elevator2 - 1
                            if elevator2 == floornum-1:
                                e2status = 'up'
                            elif elevator2 == 0:
                                e2status = 'down'
                            elif outputs[5] == 1:
                                e2status = 'up'
                            else:
                                e2status = 'down'
                            #no check here. same
                            e2dir = 'n'
                            if stop(elevator2,elevator2p,e2status,floorlist):
                                elevator2d = True
                                e2stoptime = 5
                            else:
                                e2stoptime = 0
                                e2move = False
                                elevator2d = False
                                e2status = 'neutral'
                        else:
                            if e2dir == 'down':
                                elevator2 = elevator2 - 1
                                # print('going down')
                                if elevator2 < 1:
                                    elevator2 = 0
                                    # print('reached bottom floor')
                                    e2status = 'up'
                                    e2dir = 'n'
                                    if stop(elevator2,elevator2p,e2status,floorlist):
                                        elevator2d = True
                                        e2stoptime = 5
                                    else:
                                        e2stoptime = 0
                                        elevator2d = False
                                        e2move = False
                                        e2status = 'neutral'
                            else:
                                # print('wrong direction! stopping elevator')
                                e2dir = 'down'
                                elevator2 = elevator2 + 1
                                #check
                                e2dir = 'n'
                                if stop(elevator2,elevator2p,e2status,floorlist):
                                    elevator2d = True
                                    e2stoptime = 5
                                else:
                                    e2stoptime = 0
                                    elevator2d = False
                                    e2move = False
                                    e2status = 'neutral'
        # print(time.time()-tr)
        time.sleep(1)
    #####REMOVE
    return points


# pygame.init()
# screen = pygame.display.set_mode((1000, 700))
# screen.fill('black')
# time.sleep(10)
# pygame.quit()