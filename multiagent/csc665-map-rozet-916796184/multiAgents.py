# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        if successorGameState.isWin():
            return float("inf") - 20
        # gets the manhattan dist between ghost position and new position
        dist = util.manhattanDistance(currentGameState.getGhostPosition(1), newPos)
        score = max(dist, 3) + successorGameState.getScore()
        closestFood = 100
        for food in newFood.asList():
            # gets the manhattan dist between food position and new position
            dist = util.manhattanDistance(food, newPos)
            if (dist < closestFood):
                closestFood = dist
        # calculates the scores
        if (currentGameState.getNumFood() > successorGameState.getNumFood()):
            score += 100
        if action == Directions.STOP:
            score -= 3
        score -= 3 * closestFood
        if successorGameState.getPacmanPosition() in currentGameState.getCapsules():
            score += 120
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        self.PACMAN = 0
        action = self.max_value(gameState, 0)
        return action

    def max_value(self, gameState, depth):
        if gameState.isLose() or gameState.isWin():
            return gameState.getScore()
        # get pacman's actions
        actions = gameState.getLegalActions(self.PACMAN)
        highestScore = float("-inf")

        preferred = Directions.STOP
        for action in actions:
            # recursively get pacmans score
            score = self.min_value(gameState.generateSuccessor(self.PACMAN, action), depth, 1)
            if score > highestScore:
                highestScore = score
                preferred = action

        if depth == 0:
            return preferred
        else:
            return highestScore

    def min_value(self, gameState, depth, agent):
        if gameState.isLose() or gameState.isWin():
            return gameState.getScore()

        # get next agent
        nextAgent = agent + 1
        if agent == gameState.getNumAgents() - 1:
            nextAgent = self.PACMAN

        highestScore = float("inf")

        for action in gameState.getLegalActions(agent):
            # pacman is the last agent
            if nextAgent == self.PACMAN:
                if depth == self.depth - 1:
                    # set scores at the leaf nodes
                    score = self.evaluationFunction(gameState.generateSuccessor(agent, action))
                else:
                    # next is pacman
                    score = self.max_value(gameState.generateSuccessor(agent, action), depth+1)
            # all the ghosts except pacman
            else:
                score = self.min_value(gameState.generateSuccessor(agent, action), depth, nextAgent)

            highestScore = min(score, highestScore)
        return highestScore

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        self.PACMAN = 0
        action = self.max_value(gameState, 0, float("-inf"), float("inf"))
        return action

    def max_value(self, gameState, depth, alpha, beta):
        if gameState.isLose() or gameState.isWin():
            return gameState.getScore()
        # get pacman's actions
        actions = gameState.getLegalActions(self.PACMAN)
        highestScore = float("-inf")

        preferred = Directions.STOP
        for action in actions:
            # recursively get pacmans score
            score = self.min_value(gameState.generateSuccessor(self.PACMAN, action), depth, 1, alpha, beta)
            if score > highestScore:
                highestScore = score
                preferred = action
            # calculate new alpha
            alpha = max(alpha, highestScore)
            if highestScore > beta:
                return highestScore

        if depth == 0:
            return preferred
        else:
            return highestScore

    def min_value(self, gameState, depth, agent, alpha, beta):
        if gameState.isLose() or gameState.isWin():
            return gameState.getScore()

        # get next agent
        nextAgent = agent + 1
        if agent == gameState.getNumAgents() - 1:
            nextAgent = self.PACMAN

        highestScore = float("inf")

        for action in gameState.getLegalActions(agent):
            # pacman is the last agent
            if nextAgent == self.PACMAN:
                if depth == self.depth - 1:
                    # set scores at the leaf nodes
                    score = self.evaluationFunction(gameState.generateSuccessor(agent, action))
                else:
                    # next is pacman
                    score = self.max_value(gameState.generateSuccessor(agent, action), depth+1, alpha, beta)
            # all the ghosts except pacman
            else:
                score = self.min_value(gameState.generateSuccessor(agent, action), depth, nextAgent, alpha, beta)

            highestScore = min(score, highestScore)
            # calculate new beta
            beta = min(beta, highestScore)

            if highestScore < alpha:
                return highestScore
        return highestScore

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        preferred = Directions.STOP
        score = float("-inf")

        # iterates to find the highest score
        for action in gameState.getLegalActions(0):
            nextState = gameState.generateSuccessor(0, action)
            prevScore = score
            score = max(score, self.expectedValue(nextState, 1, self.depth))
            if score > prevScore:
                preferred = action
        return preferred

    def expectedValue(self, gameState, index, depth):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        legalActions = gameState.getLegalActions(index)
        numOfActions = len(legalActions)
        totalValue = 0

        # iterates through the actions and alters the total value
        for action in legalActions:
            nextState = gameState.generateSuccessor(index, action)
            if (index == (gameState.getNumAgents()-1)):
                totalValue += self.maxValue(nextState, depth-1)
            else:
                totalValue += self.expectedValue(nextState, index+1, depth)
        return totalValue / numOfActions

    def maxValue(self, gameState, depth):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        highestScore = float("-inf")
        # iterates to recursively find the highest score
        for action in gameState.getLegalActions(0):
            nextState = gameState.generateSuccessor(0, action)
            highestScore = max(highestScore, self.expectedValue(nextState, 1, depth))
        return highestScore

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    foodDist = []
    currentPosition = list(currentGameState.getPacmanPosition())

    # iterates through all the food
    for food in currentGameState.getFood().asList():
        distance = manhattanDistance(food, currentPosition)
        # adds the distance to the food to the list
        foodDist.append(-1 * distance)

    if not foodDist:
        foodDist.append(0)
    return max(foodDist) + currentGameState.getScore()

# Abbreviation
better = betterEvaluationFunction
