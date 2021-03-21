from constants import *
import numpy as np
import time

def checkCurrent(board,color_max,color_min):
    myCorners = 0
    oppCorners = 0
    if board[0][0] == color_max:
        myCorners += 1
    elif board[0][0] == color_min:
        oppCorners += 1
    if board[0][7] == color_max:
        myCorners += 1
    elif board[0][7] == color_min:
        oppCorners += 1
    if board[7][0] == color_max:
        myCorners += 1
    elif board[7][0] == color_min:
        oppCorners += 1
    if board[7][7] == color_max:
        myCorners += 1
    elif board[7][7] == color_min:
        oppCorners += 1
    return(myCorners,oppCorners)


def checkPossible(board,color_max,color_min):
    myPossible = 0
    oppPossible = 0
    for element in board:
        if element == color_max:
           myPossible +=1
           
        elif element == color_min:
            oppPossible +=1
    
    return (myPossible,oppPossible)
    

def calcValue(capturedMax,capturedMin,possibleMax,possibleMin):
    maxCornerHeuristic = 0.6*capturedMax + 0.4*possibleMax
    minCornerHeuristic = 0.6*capturedMin + 0.4*possibleMin
    if maxCornerHeuristic+minCornerHeuristic > 0:
        cornerHeuristicVal = 100*(maxCornerHeuristic-minCornerHeuristic)/(maxCornerHeuristic+minCornerHeuristic)
    else: cornerHeuristicVal = 0
    return(cornerHeuristicVal)

def corners_heuristic(board, color_max, weight):
    if color_max == blackChar: color_min = whiteChar
    else: color_min = blackChar
    (capturedMax, capturedMin) = checkCurrent(board,color_max,color_min)     
    # ^ check corners already captured
    
    boardFeasibleUpperLeft = np.array([board[0][0], board[0][6],board[1][6], board[1][7]])
    boardFeasibleUpperRight = np.array([board[0][7], board[0][6], board[1][6], board[1][7]])
    boardFeasibleLowerLeft = np.array([board[7][0], board[7][1], board[6][0], board[6][1]])
    boardFeasibleLowerRight = np.array([board[7][7], board[7][6], board[6][6], board[6][7]])
    borders = np.array([boardFeasibleUpperLeft,boardFeasibleUpperRight,boardFeasibleLowerLeft,boardFeasibleLowerRight])
    #^borders is an array made of arrays containing the positions next to the corners
    
    nearMax = 0
    nearMin = 0
    for element in borders:
        if element[0] == '.':
            (mNear,oppNear) = checkPossible(element[1:],color_max,color_min)
            # ^ checks values of uncaptured positions next to the corners
            nearMax += mNear
            nearMin += oppNear
    

    cornersHeuristicVal = calcValue(capturedMax,capturedMin,nearMax,nearMin)*weight
    return (cornersHeuristicVal)
    

   
    