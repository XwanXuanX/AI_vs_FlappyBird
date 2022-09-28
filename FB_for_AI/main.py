# import modules
import AI as AI
import FB_for_AI as FB
import threading
from pynput.keyboard import Controller
from time import sleep


#________________________________________________________________
#   Thread 1: Create and run the game 10 times every generation
#   Thread 2: AI mimic keyboard input

# create and run a new game, exit when gameover; For every generation
def StartGame():
    for i in range(10):
        player = FB.AIPlayer(True)
        player.CreateGame()
    return

# when game is not over, mimic keyborad input; exit when gameover
def StartPlay():
    keyboard = Controller()
    key = " "

    while True:
        if gameThread.is_alive() and FB.should_jump == True:
            keyboard.press(key)
            keyboard.release(key)
            sleep(0.4)
        elif gameThread.is_alive() and FB.should_jump == False: pass
        else: return

# Multithread class: call different functions based on thread name
class AIThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("Starting " + self.name)
        if self.name == "GameThread":   StartGame()
        elif self.name == "AIThread":   StartPlay()
        print("Exiting " + self.name)

#_________________________________________________________________
#   Main Function for testing (Will be commented out later)

if __name__ == "__main__":
    gameThread = AIThread(1, "GameThread")
    aiThread = AIThread(2, "AIThread")
    gameThread.start()
    aiThread.start()

#_________________________________________________________________