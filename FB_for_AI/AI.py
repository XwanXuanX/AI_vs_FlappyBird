# import modules
import numpy as np
import random
from math import floor

#____________________________________________________________________
#                       Weight & Bias Class

class WnB:
    def __init__(self, W_list, B_list):
        self.__W_list = W_list
        self.__B_list = B_list

    def getLayerW(self, layer):
        if layer > len(self.__W_list): 
            print("Layer does not exist!")
            raise IndexError
        else: return self.__W_list[layer - 1]

    def getLayerB(self, layer):
        if layer > len(self.__B_list):
            print("Layer does not exist!")
            raise IndexError
        else: return self.__B_list[layer - 1]

#____________________________________________________________________
#                           Layer Class

# Activation functions
def sigmoid(x): return (1 / (1 + np.exp(-x)))
def tanh(x):    return (2 / (1 + np.exp(-2 * x)) - 1)
def Relu(x):    return (np.maximum(0, x))
def Softmax(x): return (np.exp(x) / np.sum(np.exp(x)))

# Dense layer class
class Layer:
    def __init__(self, units, nextUnits, activation=None, RndGene=True, W_ex=None, B_ex=None):
        self.__units = units
        self.__nextUnits = nextUnits
        self.__activation = activation
        self.__RndGene = RndGene

        if self.__RndGene == True:
            self.__W = np.random.randn(self.__units, self.__nextUnits) * 0.01
            self.__B = np.random.randn(1, self.__nextUnits) * 0.01
        else:
            self.__W = W_ex
            self.__B = B_ex

    def __useActivation(self, input):
        if self.__activation == "relu":     return Relu(input)
        if self.__activation == "tanh":     return tanh(input)
        if self.__activation == "softmax":  return Softmax(input)
        if self.__activation == "sigmoid":  return sigmoid(input)

    def Calculate(self, input):
        output = np.dot(input, self.__W) + self.__B
        output = self.__useActivation(output)
        return output

    def __Alternate_MUT(self, Weight_only=True):
        self.__W[random.randint(a=0, b=(self.__W.shape[0]-1)), 
                 random.randint(a=0, b=(self.__W.shape[1]-1))] += (2 * random.random() - 1)
        if Weight_only == False:
            self.__B[random.randint(a=0, b=(self.__B.shape[0]-1)), 
                     random.randint(a=0, b=(self.__B.shape[1]-1))] += (2 * random.random() - 1)

    def __Exchange_MUT(self, Weight_only=True):
        getPos = lambda row_num, col_num: \
            [random.randint(a=0, b=(row_num - 1)), random.randint(a=0, b=(col_num - 1))]
        
        Pos1 = getPos(self.__W.shape[0], self.__W.shape[1])
        Pos2 = getPos(self.__W.shape[0], self.__W.shape[1])
        self.__W[Pos1[0], Pos1[1]], self.__W[Pos2[0], Pos2[1]] = self.__W[Pos2[0], Pos2[1]], self.__W[Pos1[0], Pos1[1]]

        if Weight_only == False:
            Pos1 = getPos(self.__B.shape[0], self.__B.shape[1])
            Pos2 = getPos(self.__B.shape[0], self.__B.shape[1])
            self.__B[Pos1[0], Pos1[1]], self.__B[Pos2[0], Pos2[1]] = self.__B[Pos2[0], Pos2[1]], self.__B[Pos1[0], Pos1[1]]

    def mutate(self, MutTimes=1, MutType="Alternate", MutBias=False):
        if MutType == "Alternate":
            for i in range(MutTimes): self.__Alternate_MUT(Weight_only=(not MutBias))
        elif MutType == "Exchange":
            for i in range(MutTimes): self.__Exchange_MUT(Weight_only=(not MutBias))
        elif MutType == "Both":
            for i in range(MutTimes): self.__Alternate_MUT(Weight_only=(not MutBias))
            for i in range(MutTimes): self.__Exchange_MUT(Weight_only=(not MutBias))
        else: 
            print("Wrong mutation type. Mutation skipped.\n")

    # getters (if need any)
    # return the number of nodes
    def getUnits(self):     return self.__units
    # return weight
    def getWeight(self):    return self.__W
    # return bias
    def getBias(self):      return self.__B


#____________________________________________________________________
#                           Model Class

class Model:
    # define layer structure (3 -> 5 -> 3 -> 2)
    def __init__(self, RNG=True, WB=None):
        self.__input =  Layer(units=3, nextUnits=5,  # 3 -> 5
                              activation='sigmoid',
                              RndGene=RNG,
                              W_ex=None if RNG else WB.getLayerW(1), B_ex=None if RNG else WB.getLayerB(1))
        self.__dense1 = Layer(units=5, nextUnits=3,  # 5 -> 3
                              activation='relu',
                              RndGene=RNG,
                              W_ex=None if RNG else WB.getLayerW(2), B_ex=None if RNG else WB.getLayerB(2))
        self.__dense2 = Layer(units=3, nextUnits=2,  # 3 -> 2
                              activation='softmax',
                              RndGene=RNG,
                              W_ex=None if RNG else WB.getLayerW(3), B_ex=None if RNG else WB.getLayerB(3))

        if RNG == False: self.__WnB = WB
        else:
            W_list = [self.__input.getWeight(), self.__dense1.getWeight(), self.__dense2.getWeight()]
            B_list = [self.__input.getBias(),   self.__dense1.getBias(),   self.__dense2.getBias()  ]
            self.__WnB = WnB(W_list, B_list)

    def predict(self, input):
        output = self.__input.Calculate(input)
        output = self.__dense1.Calculate(output)
        output = self.__dense2.Calculate(output)
        tmpDict = {0: True, 1: False}   # 0: Jump | 1: DoNothing
        return tmpDict[output.argmax()]

    def mutate(self, MUTPercent=10):
        getTime = lambda layer, percent: \
            floor(np.size(self.__WnB.getLayerW(layer)) * (percent / 100))

        getType = lambda percent: \
            "Both" if random.randint(0, 100) < percent else \
                "Alternate" if random.randint(0, 1) else "Exchange"

        getBias = lambda percent: \
            True if random.randint(0, 100) < percent else False

        self.__input.mutate(getTime(1, MUTPercent), getType(MUTPercent), getBias(MUTPercent))
        self.__dense1.mutate(getTime(2, MUTPercent), getType(MUTPercent), getBias(MUTPercent))
        self.__dense2.mutate(getTime(3, MUTPercent), getType(MUTPercent), getBias(MUTPercent))

        del self.__WnB
        W_list = [self.__input.getWeight(), self.__dense1.getWeight(), self.__dense2.getWeight()]
        B_list = [self.__input.getBias(),   self.__dense1.getBias(),   self.__dense2.getBias()  ]
        self.__WnB = WnB(W_list, B_list)

    def getWB(self):
        return self.__WnB

