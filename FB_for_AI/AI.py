# import modules
import numpy as np
import math
import random

#____________________________________________________________________
#                           Layer Class
def sigmoid(x): return (1 / (1 + np.exp(-x)))
def tanh(x):    return (2 / (1 + np.exp(-2 * x)) - 1)
def Relu(x):    return (np.maximum(0, x))
def Softmax(x): return (np.exp(x) / np.sum(np.exp(x)))

class Layer:
    def __init__(self, units, nextUnits, activation=None, use_bias=True):
        self.__units = units
        self.__nextUnits = nextUnits
        self.__activation = activation
        self.__use_bias = use_bias

        self.__W = np.random.normal(loc=0.0, 
                                    scale=0.1, 
                                    size=(self.__units, self.__nextUnits))
        if self.__use_bias == True:
            self.__B = np.random.normal(loc=0.0, 
                                        scale=0.3,
                                        size=(self.__nextUnits))
        else: pass
    
    def __useActivation(self, input):
        if self.__activation == "relu":     return Relu(input)
        if self.__activation == "tanh":     return tanh(input)
        if self.__activation == "softmax":  return Softmax(input)
        if self.__activation == "sigmoid":  return sigmoid(input)

    def Calculate(self, input):
        output = np.matmul()

    # getters
    def getUnits(self):     return self.__units
    def getWeight(self):    return self.__W
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
