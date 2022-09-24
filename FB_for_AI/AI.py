# import modules
import numpy as np
import random

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
            self.__W = np.random.normal(loc=0.0, 
                                        scale=0.1, 
                                        size=(self.__units, self.__nextUnits))
            self.__B = np.random.normal(loc=0.0, 
                                        scale=0.3,
                                        size=(self.__nextUnits))
        else:
            self.__W = W_ex
            self.__B = B_ex

    def __useActivation(self, input):
        if self.__activation == "relu":     return Relu(input)
        if self.__activation == "tanh":     return tanh(input)
        if self.__activation == "softmax":  return Softmax(input)
        if self.__activation == "sigmoid":  return sigmoid(input)

    def Calculate(self, input):
        output = np.matmul(input, self.__W) + self.__B
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

    def mutate(self, extent):
        

    # getters
    # return the number of nodes
    def getUnits(self):     return self.__units
    # return weight
    def getWeight(self):    return self.__W
    # return bias
    def getBias(self):      return self.__B


#____________________________________________________________________
#                           Model Class


#___________________________________________________________________
#                           AI Class
# Side Notes:
#   * AI class may contain variables:
#       * self.Generation
#       * self.IDNumber
#       * self.score
#       * self.isDead
#       * self.model
#
#   * AI class may contain methods:
#       * __init()__
#       * mutate()
#       * play()
#       * breed()

layer = Layer(units=3, nextUnits=10, activation="relu", RndGene=True)
layer.mutate(1)
