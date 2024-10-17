import nn
import simulation as simul
import random
import torch
import animation

def casegeneration(floor):
    e1pos = random.randint(0,floor-1)
    e2pos = random.randint(0,floor-1)
    buttonlistup = []
    buttonlistdown = []
    e1buttonlist = [0]*floor
    e2buttonlist = [0]*floor
    for _ in range(floor):
        if random.randint(0,5) == 0:
            buttonlistup.append(1)
        else:
            buttonlistup.append(0)
    for _ in range(floor):
        if random.randint(0,5) == 0:
            buttonlistdown.append(1)
        else:
            buttonlistdown.append(0)
    if random.randint(0,1) == 0:
        e1statusint = 1
        e1dirint = 1
        for i in range(e1pos,8):
            if random.randint(0,4) == 0:
                e1buttonlist[i+1] = 1
    else:
        e1statusint = -1
        e1dirint = -1
        for i in range(0,e1pos):
            if random.randint(0,4) == 0:
                e1buttonlist[i] = 1
    if random.randint(0,1) == 0:
        e2statusint = 1
        e2dirint = 1
        for i in range(e2pos,8):
            if random.randint(0,4) == 0:
                e2buttonlist[i+1] = 1
    else:
        e2statusint = -1
        e2dirint = -1
        for i in range(0,e2pos):
            if random.randint(0,4) == 0:
                e2buttonlist[i] = 1     

    buttonlistup[e1pos] = 0
    buttonlistup[e2pos] = 0
    buttonlistdown[e1pos] = 0
    buttonlistdown[e2pos] = 0
    inputlist = [0].copy()*floor*2
    inputlist[e1pos] = 1
    inputlist[e2pos+floor] = 1
    inputlist.extend(buttonlistup)
    inputlist.extend(buttonlistdown)
    inputlist.extend(e1buttonlist)
    inputlist.extend(e2buttonlist)
    e1dint = 0
    e2dint = 0
    if random.randint(0,3) == 0:
        e1dint = 1
    if random.randint(0,3) == 0:
        e2dint = 1
    if random.randint(0,2) != 0:
        e1dirint = 0
    if random.randint(0,2) != 0:
        e2dirint = 0
    if not 1 in e1buttonlist:
        e1statusint = 0
    if not 1 in e2buttonlist:
        e2statusint = 0
    inputlist.extend([e1statusint,e2statusint,e1dint,e2dint,e1dirint,e2dirint])
    return inputlist


def simulatepopulation(nnlist,personlist,floornum):
    outputlist = []
    for neural in nnlist:
        outputlist.append(simul.simulate(neural,personlist,floornum))
        # print('completed simulation, '+str(len(outputlist))+' out of '+str(len(nnlist)))
    print('test')
    return outputlist

def crossoverpopulation(nnlist,fitnesslist,floornum):
    childlist = []
    sortinglist = []
    for i in range(len(nnlist)):
        sortinglist.append((fitnesslist[i],nnlist[i]))
    sortinglist.sort(key = lambda x: x[0])
    sortinglist.reverse()
    tuplelist = []
    x = 20
    y = 0
    for _ in range(20):
        for _ in range(x):
            tuplelist.append((x,y))
            y += 1
        x = x - 1
        y = 0
    for t in tuplelist:
        childlist.append(nn.crossover(sortinglist[t[0]][1],sortinglist[t[1]][1],0.8,floornum))
    for i in range(5):
        childlist.append(sortinglist[i][1])
    return childlist

floor = 9

def genlist(floornum):
    personlist = []
    for _ in range(100):
        personlist.append((random.randint(0,3599),random.randint(0,floornum-1),random.randint(0,floornum-1)))
    return personlist

def saveweights(network,filename):
    file = open(filename,'w')
    outlist = network.getweight()
    file.write(str(outlist))
    file.close

def loadweights(filename,floor):
    file = open(filename,'r')
    inlist = eval(file.read())
    wblist = []
    for element in inlist:
        wblist.append(torch.Tensor(element))
    network = nn.getmodel(floor)
    network.defweight(wblist)
    return network

# paslist = []
# for _ in range(100):
#     start = random.randint(0,8)
#     out = start
#     while out == start:
#         out = random.randint(0,8)
#     paslist.append((random.randint(0,1799),start,out))    
f = open('paslist.txt','r')
paslist = eval(f.read())
f.close()
model = loadweights('gradient5.txt',floor)
testing = True
animation.simulate(model,paslist,floor)
assert False

