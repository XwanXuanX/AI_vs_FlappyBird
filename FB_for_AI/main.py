# import modules
import FB_for_AI as FB
from threading import Thread
from pynput.keyboard import Controller
from time import sleep
from random import randint

NUMBER_OF_PLAYERS = 10 


#__________________________________________________________________
#   Player thread class
#   when game is not over, mimic keyborad input; exit when gameover
class AIPlayerThread(Thread):
    run = True

    def __init__(self, threadName):
        Thread.__init__(self)
        self.__threadName = threadName

    def run(self):
        print("Starting: ", self.__threadName)

        keyboard = Controller()
        key = " "
        while self.run:
            if FB.should_jump == True:
                keyboard.press(key)
                keyboard.release(key)
                sleep(0.5)
            elif FB.should_jump == False: pass

    def StopThread(self):
        print("Closing: ", self.__threadName)
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

    def __SelectBest(self):
        





#_________________________________________________________________
#   Main Function for testing (Will be commented out later)

if __name__ == "__main__":
    # create and run a new game, exit when gameover; For every generation
    gen = Generation()
    print(Generation.getCurrentGen())
    gen.Train() 

#_________________________________________________________________