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
from util import *

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

def translator(actions):
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST
    moves = []
    for i in actions:
        if i == 'South':
            moves.append(s)
        if i == 'North':
            moves.append(n)
        if i == 'East':
            moves.append(e)
        if i == 'West':
            moves.append(w)
    return moves

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    successors = problem.getSuccessors(problem.getStartState())
    print(successors[0][0])
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]



# def genericSearch(problem : SearchProblem, strat, state, actions = [],visited = []): #maybe add a cost function here?
#     strat.push((state, actions,0))
#     while not strat.isEmpty():
#         curr, actions, cost = strat.pop()
#         if problem.isGoalState(curr):
#             print(cost)
#             return actions
        
#         else:
#             if curr not in visited:
#                 visited.append(curr)
#                 successors = problem.getSuccessors(curr)

#                 for s in successors:
#                         strat.push((s[0], actions + [s[1]],s[2]+cost)) #fringe has ((x,y),actions,total_cost)
    
#     return actions

def genericSearch(problem : SearchProblem, strat, state, actions = []):
    visited = []
    strat.push((state,actions,0))
    while not strat.isEmpty():
        curr, hist, tot_cost = strat.pop()
        if problem.isGoalState(curr):
            return hist
        else:
            if curr not in visited:
                visited.append(curr)
                successors = problem.getSuccessors(curr)
                for s in successors:
                    strat.push((s[0],hist+[s[1]],tot_cost+s[2]))
    return False
        



def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    fringe = Stack()
    acts = genericSearch(problem,fringe,start_state)
    #moves = translator(acts)
    return  acts


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    fringe = Queue()
    acts = genericSearch(problem,fringe,start_state)
    #moves = translator(acts)
    return  acts


def helper(problem : SearchProblem,strat,state,actions = []):
    visited = []
    strat.push((state,actions),0)
    while not strat.isEmpty():
        curr, hist = strat.pop()
        if problem.isGoalState(curr):
            return hist
        else:
            if curr not in visited:
                visited.append(curr)
                successors = problem.getSuccessors(curr)
                for s in successors:
                    strat.push((s[0],hist+[s[1]]),problem.getCostOfActions(hist+[s[1]]))
    return False

    ## use problem get cost of path up to now to update priority\


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""

    #Want to use priority queue with function in it?
    #How do we take in a cost function?

    start_state = problem.getStartState()
    fringe = PriorityQueue()
    acts = helper(problem,fringe,start_state)
    #moves = translator(acts)
    return  acts


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def astarHelp(problem : SearchProblem, strat, state, heuristic, actions = []):
    visited = []
    strat.push((state,actions),0)
    while not strat.isEmpty():
        curr, hist = strat.pop()
        if problem.isGoalState(curr):
            return hist
        else:
            if curr not in visited:
                visited.append(curr)
                successors = problem.getSuccessors(curr)
                for s in successors:
                    strat.push((s[0],hist+[s[1]]),problem.getCostOfActions(hist+[s[1]])+heuristic(s[0],problem))
    return False

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    ### add heuristic to priority

    start_state = problem.getStartState()
    fringe = PriorityQueue()
    acts = astarHelp(problem,fringe,start_state,heuristic)
    #moves = translator(acts)
    return  acts


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
