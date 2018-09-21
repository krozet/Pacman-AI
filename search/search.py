# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    frontier = util.Stack()
    visited = []
    frontier.push((problem.getStartState(), None, []))

    while not frontier.isEmpty():
        node = frontier.pop()
        (position,direction,path) = node

        if position not in visited:
            # add visited location to visited set
            visited.append(position)
            if(problem.isGoalState(position)):
                return path
            # checks through each state in successor states
            for nextNode in problem.getSuccessors(position):
                (nextPosition,nextDirection,cost) = nextNode
                if nextPosition not in visited:
                    # saves the node and the path taken
                    frontier.push((nextPosition, nextDirection, path + [nextDirection]))

def breadthFirstSearch(problem):
    frontier = util.Queue()
    visited = []
    frontier.push((problem.getStartState(), None, []))

    while not frontier.isEmpty():
        node = frontier.pop()
        (position,direction,path) = node

        if position not in visited:
            # add visited location to visited set
            visited.append(position)
            if(problem.isGoalState(position)):
                return path
            # checks through each state in successor states
            for nextNode in problem.getSuccessors(position):
                (nextPosition,nextDirection,cost) = nextNode
                if nextPosition not in visited:
                    # saves the node and the path taken
                    frontier.push((nextPosition, nextDirection, path + [nextDirection]))

def uniformCostSearch(problem):
    frontier = util.PriorityQueue()
    firstNode = ((problem.getStartState(), None, 0), [], 0)
    frontier.push(firstNode, None)
    visited = set()

    while not frontier.isEmpty():
        node = frontier.pop()
        (location,path,cost) = node
        (position,direction,currCost) = location
        if problem.isGoalState(position):
            return path
        if position not in visited:
            # add visited location to visited set
            visited.add(position)
            # checks through each state in successor states
            for nextNode in problem.getSuccessors(position):
                (nextPosition,nextPath,nextCost) = nextNode
                if nextPosition not in visited:
                    # get the next priority level
                    newNode = (nextNode, path + [nextPath], cost + nextCost)
                    # saves the node and the path taken
                    frontier.push(newNode, cost + nextCost)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = util.PriorityQueue()

    visited = []
    heur = heuristic(problem.getStartState(), problem)
    currentCost = 0
    totalCost = currentCost + heur
    frontier.push((problem.getStartState(), None, currentCost, []), totalCost)

    while not frontier.isEmpty():
        node = frontier.pop()
        (position,direction,cost,path) = node
        if problem.isGoalState(position):
            return path
        if position not in visited:
            visited.append(position)
            for nextNode in problem.getSuccessors(position):
                (nextPosition,nextPath,nextCost) = nextNode
                if nextPosition not in visited:
                    heur = heuristic(nextPosition, problem)
                    currentCost = cost + nextCost
                    totalCost = currentCost + heur
                    newNode = (nextPosition, nextPath, currentCost, path + [nextPath])
                    frontier.push(newNode, totalCost)

def createActionListFromVisited(visited):
    actions = []
    startState = visited[0][0]
    print "Visited before:", visited
    visited.reverse()
    print "Visited after:", visited

    for state in visited:
        action = None
        vertex,direction = state
        if vertex == startState:
            print "BREAK"
            break
        from game import Directions
        if 'South' in direction:
            action = Directions.SOUTH
        elif 'North' in direction:
            action = Directions.NORTH
        elif 'West' in direction:
            action = Directions.WEST
        elif 'East' in direction:
            action = Directions.EAST
        if action is not None:
            actions.append(action)
    return actions

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
