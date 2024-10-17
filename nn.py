import torch
import torch.nn as nn
import random
import time

device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
print(f"Using {device} device")


class NeuralNetwork(nn.Module):
    def __init__(self,floor) -> None:
        super().__init__()
        y = floor*6 + 6
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(y, 32),
            nn.LeakyReLU(),
            nn.Linear(32, 32),
            nn.LeakyReLU(),
            nn.Linear(32, 32),
            nn.LeakyReLU(),
            nn.Linear(32, 32),
            nn.LeakyReLU(),
            nn.Linear(32, 8),
        )
    def forward(self, x):
        logits = self.linear_relu_stack(x)
        return logits

    def getweight(self):
        wblist = []
        for _, param in self.named_parameters():
            wblist.append(param.data.tolist())
        return wblist
    
    def defweight(self,wblist):
        i = 0
        for _, param in self.named_parameters():
            param.data = wblist[i]
            i += 1
        return None
    
    def getneurons(self):
        l = []
        for _, module in self.named_modules():
            try:
                l.append(module.out_features)
            except:
                pass
        return l

    def getinputs(self):
        l = []
        for _, module in self.named_modules():
            try:
                l.append(module.in_features)
            except:
                pass
        return l

def getmodel(floor):
    return NeuralNetwork(floor).to(device)



# avg = 0
# for _ in range(100):
#     X = torch.rand(212, device=device)
#     print(X)
#     t = time.time()
#     logits = model(X)
#     t = time.time() - t
#     avg += t
# print(avg/100)


def crossover(nn1,nn2,mutationrate,floor):
    #gets the number of neurons
    neuronnum = 0
    for i in nn1.getneurons():
        neuronnum += i
    #creates a list of 1 and 2
    temp = [1]
    neurallist = temp.copy()*(neuronnum//2)
    temp = [2]
    neurallist.extend(temp.copy()*(neuronnum//2))
    child = NeuralNetwork(floor).to(device)
    childweightlist = []
    input = nn1.getinputs()
    #enter a loop of assigning neurons from nn1 or nn2 to the child network, with mutation.
    for i in range(len(nn1.getneurons())):
        neurons = nn1.getneurons()[i]
        childweight = []
        childbias = []
        weight1 = nn1.getweight()[i*2]
        bias1 = nn1.getweight()[i*2 + 1]
        weight2 = nn2.getweight()[i*2]
        bias2 = nn2.getweight()[i*2 + 1]
        for j in range(neurons):
            if random.random() < mutationrate:
                childweight.append(torch.normal(0.0,0.1,(input[i],)).tolist())
                childbias.append(random.normalvariate(0,1))
            elif random.randint(0,1) == 0:
                childweight.append(weight1[j])
                childbias.append(bias1[j])
            else:
                childweight.append(weight2[j])
                childbias.append(bias2[j])
        temp = torch.Tensor(childweight)
        childweightlist.append(temp)
        childweightlist.append(torch.Tensor(childbias))
    child.defweight(childweightlist)
    return child

