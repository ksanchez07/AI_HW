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

#for dfs
from util import Stack

#for bfs
from util import Queue

#for usc / A-Star
from util import PriorityQueue

#for A-Star

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
    stack = Stack()

    #(0,0)
    start = problem.getStartState()
    stack.push((start, 0, [])) 

    #what its passed so far
    passed = set()

    #runs until path is explored
    while not stack.isEmpty():

        #gets current path
        state, hitWalls, actions = stack.pop()

        if problem.isGoalState(state):
            if 1 <= hitWalls <= 2:
                return actions 
            
            #reached max walls able to hit so dont phase anymore
            continue 

        #adds the passed path so far so it wont repeat
        if (state, hitWalls) not in passed:
            passed.add((state, hitWalls))

            for successor, action, stepCost in problem.getSuccessors(state):

                
                temp = hitWalls  
                if problem.isWall(successor):  
                    temp += 1  

                    #can only hit wall up to twice
                if temp <= 2:  
                    stack.push((successor, temp, actions + [action]))  

    #no solution
    return []  

def breadthFirstSearch(problem):
    #same code as dfs but replace everything with queue
    queue = Queue()

    #(0,0)
    start = problem.getStartState()
    queue.push((start, 0, [])) 

    #what its passed so far
    passed = set()

    #runs until path is explored
    while not queue.isEmpty():

        #gets current path
        state, hitWalls, actions = queue.pop()

        if problem.isGoalState(state):
            if 1 <= hitWalls <= 2:
                return actions 
            
            #reached max walls able to hit so dont phase anymore
            continue 

        #adds the passed path so far so it wont repeat
        if (state, hitWalls) not in passed:
            passed.add((state, hitWalls))

            for successor, action, stepCost in problem.getSuccessors(state):

                
                temp = hitWalls  
                if problem.isWall(successor):  
                    temp += 1  

                    #can only hit wall up to twice
                if temp <= 2:  
                    queue.push((successor, temp, actions + [action]))  

    #no solution
    return []  




def uniformCostSearch(problem):

    priorityQueue = PriorityQueue()
    start = problem.getStartState()

    #adding cost and priority value to it
    priorityQueue.push((start, 0, [], 0), 0)  
    passed = {}

    while not priorityQueue.isEmpty():
        state, hitWalls, actions, cost = priorityQueue.pop()

        if problem.isGoalState(state):
            if 1 <= hitWalls <= 2:
                return actions 
            continue

        #until here, it was pretty much the same as dfs and bfs but now we have to factor in costs
        
        #checks wall condition and if its the cheapest path
        if (state, hitWalls) not in passed or cost < passed[(state, hitWalls)]:
            #min cost
            passed[(state, hitWalls)] = cost

            for successor, action, stepCost in problem.getSuccessors(state):
                if hitWalls < 2 or not problem.isWall(successor):
                    temp = hitWalls + problem.isWall(successor)
                    newCost = cost + stepCost
                    priorityQueue.push((successor, temp, actions + [action], newCost), newCost)
   
    #no solution
    return []  



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    priorityQueue = PriorityQueue()
    startState = problem.getStartState()

    #adding cost and priority value to it
    priorityQueue.push((startState, 0, [], 0), 0) 
    visited = {}

    while not priorityQueue.isEmpty():
        state, hitWalls, actions, cost = priorityQueue.pop()

        if problem.isGoalState(state):
            if 1 <= hitWalls <= 2:
                return actions  
            continue

        #up to here it was pretty much same as ucs but now with hueristic costs

        if (state, hitWalls) not in visited or cost < visited[(state, hitWalls)]:
            visited[(state, hitWalls)] = cost

            for successor, action, stepCost in problem.getSuccessors(state):

                if hitWalls < 2 or not problem.isWall(successor):

                    tempWalls = hitWalls + problem.isWall(successor)
                    tempCost = cost + stepCost
                    totalCost = tempCost + heuristic(successor, problem)
                    priorityQueue.push((successor, tempWalls, actions + [action], tempCost), totalCost)

    #no solution
    return []  




# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
