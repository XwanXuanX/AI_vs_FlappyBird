# import modules
import numpy as np
import FB_for_AI as FB
from threading import Thread
from pynput.keyboard import Controller
from time import sleep
from random import randint
from AI import WnB
from matplotlib import pyplot as plt

NUMBER_OF_PLAYERS = 10 
NUMBER_OF_BEST    = 3

TRAIN_GENERATION = 2

Fitness_Graph = []

#__________________________________________________________________
#   Player thread class
#   when game is not over, mimic keyborad input; exit when gameover
class AIPlayerThread(Thread):
    run = True

    def __init__(self, threadName):
        Thread.__init__(self)
        self.__threadName = threadName

    def run(self):
        keyboard = Controller()
        key = " "
        while self.run:
            if FB.should_jump == True:
                keyboard.press(key)
                keyboard.release(key)
                sleep(0.5)
            elif FB.should_jump == False: pass

    def StopThread(self):
        self.run = False


#_________________________________________________________________
#           Generation Class (1 Gen = 30 Players)

class Generation:
    # This variable record the current generation number
    # It will +=1 whenever one generation finished
    __Current_Gen = 0
    # This variable holds the breed results of the previous generation
    # It will be assigned to new players in the next generation
    __Prev_WBList = []

    # setters and getters for shared class variables
    def getCurrentGen(): return Generation.__Current_Gen
    def getPrevWBList(): return Generation.__Prev_WBList
    def setPrevWBList(WBList):
        Generation.__Prev_WBList = WBList

    def __init__(self):
        Generation.__Current_Gen += 1   # When a generation is created, increament

        # Create an empty list to hold the total 30 AI players
        self.__PlayerList = []

    def Train(self):
        for i in range(NUMBER_OF_PLAYERS):
            PlayerThread = AIPlayerThread("Player Thread")  # Create thread to mimic keyboard input

            # initialize players based on generation
            if Generation.__Current_Gen == 1:
                player = FB.AIPlayer(True)
            else:
                player = FB.AIPlayer(False, Generation.__Prev_WBList[randint(0, len(Generation.__Prev_WBList) - 1)])

            PlayerThread.start()
            player.CreateGame()
            PlayerThread.StopThread()

            self.__PlayerList.append(player)
            print("Player ", str(i + 1), ": ", str(player.fitness), " point(s)")

    def __SelectBest(self):
        TmpFitness = []
        BestPlayer = []

        # Put every score into a list
        for player in self.__PlayerList: TmpFitness.append(player.fitness)
        # The players with the top scores are put into BestPlayer list
        for i in range(NUMBER_OF_BEST):
            index = TmpFitness.index(max(TmpFitness))   # Get the index of the biggest value in score list
            BestPlayer.append(self.__PlayerList[index]) # Put the top player in the best player list
            del TmpFitness[index]   # Delete the top value found in this round

        BestWnB = []
        for WB in BestPlayer: BestWnB.append(WB.model.getWB()) # put the WnB of each best model into a list
        return BestWnB

    def Crossover(self):
        BestModels = self.__SelectBest() # holds the WnB classes of top three models
        Crossed = []                     # holds the result of crossover

        for i in range(len(BestModels)):
            for j in range(len(BestModels)):
                if i >= j:
                    continue

                new_WList = []
                new_BList = []
                # Crossover for each layer
                for k in range(3):
                    layer_IW, layer_IB = BestModels[i].getLayerW(k + 1), BestModels[i].getLayerB(k + 1)
                    layer_JW, layer_JB = BestModels[j].getLayerW(k + 1), BestModels[j].getLayerB(k + 1)

                    layer_newW = np.zeros(layer_IW.shape)   # new weight layer
                    layer_newB = np.zeros(layer_IB.shape)   # new bias layer

                    # Crossover weight matrix
                    for col in range(layer_newW.shape[1]):
                        sel_dict = \
                        {
                            0: layer_IW[:,col], 
                            1: layer_JW[:,col]
                        }
                        layer_newW[:,col] = sel_dict[randint(0, 1)]
                    
                    # Crossover bias matrix
                    for col in range(layer_newB.shape[1]):
                        sel_dict = \
                        {
                            0: layer_IB[:, col],
                            1: layer_JB[:, col]
                        }
                        layer_newB[:,col] = sel_dict[randint(0, 1)]
                    
                    new_WList.append(layer_newW)
                    new_BList.append(layer_newB)
                
                tmpWB = WnB(new_WList, new_BList)
                Crossed.append(tmpWB)
        
        Generation.__Prev_WBList = Crossed
    
    def Write2File(self):
        BestModels = self.__SelectBest()

        with open("C:\\七零八碎\\编程\\VSCode\\AI_vs_FlappyBird\\FB_for_AI\\Best_WnB.txt", "w") as file:
            for layer in range(3):
                layer_W = BestModels[0].getLayerW(layer + 1)
                layer_B = BestModels[0].getLayerB(layer + 1)

                file.write("Layer " + str(layer) + "____________________________________________________________" + "\n")
                file.write("Weight: \n")
                file.write("Shape: " + str(layer_W.shape) + "\n")
                file.write("Param: " + str(layer_W) + "\n")
                file.write("Bias: \n")
                file.write("Shape: " + str(layer_B.shape) + "\n")
                file.write("Param: " + str(layer_B) + "\n")
                file.write("\n")
    
    def GenFitnessMean(self):
        Fitness = []
        for player in self.__PlayerList: Fitness.append(player.fitness)
        Fitness_Graph.append(np.mean(Fitness))


def ShowDiagrams():
    plt.title("Fitness Curve of " + str(TRAIN_GENERATION) + " Generation(s)")
    plt.xlabel("Generation(s)")
    plt.ylabel("Ave Fitness")
    plt.plot(Fitness_Graph, label="Ave Fitness")
    plt.legend()
    plt.savefig("C:\\七零八碎\\编程\\VSCode\\AI_vs_FlappyBird\\FB_for_AI\\Fitness.png")
    plt.show()


def main():
    # create and run a new game, exit when gameover; For every generation
    for Gen in range(TRAIN_GENERATION):
        gen = Generation()
        print("__________Current Generation: ", str(Generation.getCurrentGen()), "_________")
        gen.Train()
        gen.GenFitnessMean()
        if Gen != TRAIN_GENERATION-1: gen.Crossover()
        else: gen.Write2File()
        print("\n")
    
    ShowDiagrams()


if __name__ == "__main__":
    main()
