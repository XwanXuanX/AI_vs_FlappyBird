# import modules
# import tensorflow as tf
import numpy as np
import threading
from time import sleep
from pynput.keyboard import Controller
from FB_for_AI import *

#________________________________________________________________
#   Thread 1: Create and run the game
#   Thread 2: AI mimic keyboard input

# AI will modify this global variable to decide whether to jump.
should_jump = True

# create and run a new game, exit when gameover
def StartGame():
    game = Game()
    game.CreateGame()
    if game.is_game_running == False: return

# when game is not over, mimic keyborad input; exit when gameover
def StartPlay():
    global should_jump
    keyboard = Controller()
    key = " "

    while True:
        if gameThread.is_alive() and should_jump == True:
            keyboard.press(key)
            keyboard.release(key)
            sleep(0.4)
        elif gameThread.is_alive() and should_jump == False: pass
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