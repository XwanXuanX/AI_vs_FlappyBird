# import modules
import FB_for_AI as FB
from threading import Thread
from pynput.keyboard import Controller
from time import sleep


# when game is not over, mimic keyborad input; exit when gameover
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
#   Main Function for testing (Will be commented out later)

if __name__ == "__main__":
    # create and run a new game, exit when gameover; For every generation
    for i in range(10):
        AIPlay = AIPlayerThread("Player Thread")
        player = FB.AIPlayer(True)
        AIPlay.start()
        player.CreateGame()
        AIPlay.StopThread()

#_________________________________________________________________