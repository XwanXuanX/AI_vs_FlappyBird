# AI Vs. FlappyBird
## Introduction
This is an experimental project made by XwanXuanX in about 10 days. The aim of this project is to create an AI which can play the game for a long time without dying. It may takes several generations to evolve to what it is expected to be. Detailed description of methods is given in the section below.

## Background
Flappy Bird is an arcade-style game in which the player controls the bird Faby, which moves persistently to the right. The player is tasked with navigating Faby through pairs of pipes that have equally sized gaps placed at random heights. Faby automatically descends and only ascends when the player taps the touchscreen. Each successful pass through a pair of pipes awards the player one point. Colliding with a pipe or the ground ends the gameplay.

## Theory
The basic idea of this project is evolution. But how I made it possible for a computer-created AI? First of all, I will create a generation of AI players, whose weight and bias are randomly chosen. At the point of time, those AI players have no idea of the game and how they should play it. Each AI player corresponds to a unique score (a.k.a. fitness, in evolution), and the score records the number of levels the current player passed. Scores are used to select the fittest players, and their weight and bias are used to create the next generation using the crossover method (which will be discussed later). Theoretically, each generation will gradually become better and better through time.

## Methods
Now let's talk about how everything is setup and how they work together. An `AIPlayer` class contains several sections: the `Model` class, the `Game`, and the `score`. As mentioned above, the `score` and `Game` are simply variables related to the gameplay, while the `Model` class has a lot to discuss.

As we all know, the model of an AI consists of layers, and each layer consists of a certain number of nerons. Thus, I also created a `Layer` class, which stores/initializes the weight and bias of a layer, and store the structure of the network. In the first generation, there is no previous weight and bias to be inherited from, thus all weight and bias are initialized randomly following the Binary Distribution. However, for the older generations, there weight and bias are inherited rather than randomly chosen. The `Layer` class also contains a method called `Calculate()`, which you may guess it out by its name, is used to calculate the output of the layer using linear function `y = wx + b` (w: weight, b: bias).

In the model class, four layers are created so that the structure of the model is set. The structure contains four layers, with 3(input), 5(dense1), 5(dense1), 2(output) nerons respectively. With a piece of data, final output can be calculated through forward propagation using the `Calculate()` method.

After the structure of AI player is created, it's time to create the game. My approach is to let each player create its own game, rather than restate an existing game. To accomplish this, the `AIPlayer` class must contain the main game loop, and shut the game down once gameover. Of course, it also contains the model and fitness score.

## Experiment
To conduct the experiment, many players should be created and mutate and crossover, and eventually breed the next generation. Therefore, a `Generation` class is needed. This class contains two important methods: `Train()` and `Crossover()`. The `Train()` method basically create a new game and test the player's ability, while the `Crossover()` method select the best three(customized, 3 is default) players and crossover their weight and bias matrices. The newly generatated weight and bias are store in a class variable `Generation.__Prev_WBList`, which can be accessed by any class instance.

Next, using a `for loop`, I automate the process of training, selecting, breeding, and generate the next generation. In the latest experiment, I set the epoch to 50 in order to test the ability of AI. After each generation is over, I also record the average fitness(score) of the generation. This data is used to draw a _Fitness Curve_ for each generation to visualize the learning progress. Furthermore, I also extract parameters from the best AI model and put it in to a txt file.

## Results
The result of this experiment can be directly seen from the _Fitness Curve_. According to the graph, it seems that either the AI player's learning progress is extremely slow, or the players did not learn anything at all. The average fitness of each generation jumps up and down randomly without any trend of increasing overall. This result contradicts to what is expected. Thus, I have to conclude that this experiment fails.

However, there were still some interesting findings while obsering AI playing this game. For instance, some players in the first generation may not jump at all, due to the fact that their models are randomly generated. The fitness(score) for those players are always 0, and, according to my evolution algorithm, their genes are bound to go extinct. After several generations, it can be clearly observed that the number of those players who do nothing at all continuely decrease and approaching zero. Another interesting finding is that, for once or twice, the AI tried to avoid obstacles on itself (but failed). These facts illustrate that the evolution algorithm indeed has some effects, but very minor.

## Reflection
Why this theoretically-validated theory fails in real life experiment? There are five potential reasons which lead to this outcome. Firstly, it is suspected that the data fed into the network are not strong enough for the AI player to predict its movement. In this experiment, only the bird's and the gap's Y-positions are fed into the network. However, the bird's X-position relative to the pipes are not provided. Thus the player may not know whether it is the right time to adjust its Y-Position to fly through the gap just in time. Therefore, if the experiment is to be conducted one more time, an extra X-position need to be provided which may increase the performace of players slightly.

Another potential reason may come from the `Mutate()` and `Crossover()` methods. Two types of mutations are used in the `Mutation()` method: Alternate Mutation and Exchange Mutation. However, mutation is a totally random process and neither of those mutation types are proved by mathematical formulas that they are the best mutation types to use. Using non-efficient mutations may lower the effectiveness of evolution. Similarly, the crossover process is also built upon randomness, and the random combinations of previous parameters may not likely to lead to a desired result.

Last but not least, another potential reason may come from the model structure and the randomly initialized parameters. Different from the NEAT evolution algorithm, the structure of the model is unmodifiable. Thus the currently defined model (3->5->3->2) may not likely be the best model to solve the problem. If the experiment is to be conducted one more time, different model structure should be considered. The randomly initialized parameters are likely to be the most significant reason of this failure. These parameters are initialized randomly following the binary distribution, but the used standard deviation and mean are not specified, which may lead to some strange cases (i.e. some players do nothing at all).

## Appendix
If you want to try this AI yourself, please make sure that Python is installed on your computer, along with some Python packages (i.e. numpy, pygame, sklearn).

Clone this repository to your local hard drive, navigate to `FB_for_AI/main.py`, enter the number of generations you want to train, and click run. 

If you want to try this game yourself, navigate to FB_for_human/FB_for_human.py, and click run. All you have to do is spamming the space bar and try to avoid obstacles. Enjoy and have fun.