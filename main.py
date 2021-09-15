# I found this article very helpful:
# https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/

import os, math

def GetWinner(board):
    """
    Returns the winner in the current board if there is one, otherwise it returns None.
    """
    # horizontal
    if board[0] == board[1] and board[1] == board[2]:
        return board[0]
    elif board[3] == board[4] and board[4] == board[5]:
        return board[3]
    elif board[6] == board[7] and board[7] == board[8]:
        return board[6]
    # vertical
    elif board[0] == board[3] and board[3] == board[6]:
        return board[0]
    elif board[1] == board[4] and board[4] == board[7]:
        return board[1]
    elif board[2] == board[5] and board[5] == board[8]:
        return board[2]
    # diagonal
    elif board[0] == board[4] and board[4] == board[8]:
        return board[0]
    elif board[2] == board[4] and board[4] == board[6]:
        return board[2]

def PrintBoard(board):
    """
    Clears the console and prints the current board.
    """
    os.system('cls' if os.name=='nt' else 'clear')
    print(f'''
    {board[0]}|{board[1]}|{board[2]}
    {board[3]}|{board[4]}|{board[5]}
    {board[6]}|{board[7]}|{board[8]}
    ''')

def GetAvailableCells(board):
    """
    Returns a list of indices containing all available cells in a board.
    """
    available = list()
    for cell in board:
        if cell != "X" and cell != "O":
            available.append(cell)
    return available

def minimax(position, depth, alpha, beta, isMaximizing):
    """
    The AI algorithm responsible for choosing the best move. Returns best value of a move.
    """
    # evaluate current board: if maximizing player won -> return 10 
    #                         if minimizing player won -> return -10
    #                         if no one is winning (tie) -> return 0

    # NOTE: Even though the following AI plays perfectly, it might 
    #       choose to make a move which will result in a slower victory 
    #       or a faster loss. Lets take an example and explain it
    #       Assume that there are 2 possible ways for X to win the game from a give board state.
    #       Move A : X can win in 2 move
    #       Move B : X can win in 4 moves
    #       Our evaluation will return a value of +10 for both moves A and B. Even though the move A 
    #       is better because it ensures a faster victory, our AI may choose B sometimes. To overcome 
    #       this problem we subtract the depth value from the evaluated score. This means that in case 
    #       of a victory it will choose a the victory which takes least number of moves and in case of 
    #       a loss it will try to prolong the game and play as many moves as possible.
    winner = GetWinner(position)
    if winner != None:
        return 10 - depth if winner == "X" else -10 + depth
    if len(GetAvailableCells(position)) == 0:
        return 0

    if isMaximizing:
        maxEval = -math.inf
        for cell in GetAvailableCells(position):
            position[cell - 1] = "X"
            Eval = minimax(position, depth + 1, alpha, beta, False)
            maxEval = max(maxEval, Eval)
            alpha = max(alpha, Eval)
            position[cell - 1] = cell
            if beta <= alpha:
                break # prune
        return maxEval
    else:
        minEval = +math.inf
        for cell in GetAvailableCells(position):
            position[cell - 1] = "O"
            Eval = minimax(position, depth + 1, alpha, beta, True)
            minEval = min(minEval, Eval)
            beta = min(beta, Eval)
            position[cell - 1] = cell
            if beta <= alpha:
                break # prune
        return minEval

def FindBestMove(currentPosition, AI):
    """
    This will return the best possible move for the player.
    Will Traverse all cells, evaluate minimax function for all empty cells.
    And return the cell with optimal value.

    Parameters:
        currentPosition (list): The current board to find best move for.
        AI (str): The AI Player ("X" or "O").

    Returns:
        int: Index of best move for the current position.
    """
    bestVal = -math.inf if AI == "X" else +math.inf
    bestMove = -1
    for cell in GetAvailableCells(currentPosition):
        currentPosition[cell - 1] = AI
        moveVal = minimax(currentPosition, 0, -math.inf, +math.inf, False if AI == "X" else True)
        currentPosition[cell - 1] = cell
        if (AI == "X" and moveVal > bestVal):
            bestMove = cell
            bestVal = moveVal
        elif (AI == "O" and moveVal < bestVal):
            bestMove = cell
            bestVal = moveVal
    return bestMove

def main():
    player = input("Play as X or O? ").strip().upper()
    AI = "O" if player == "X" else "X"
    currentGame = [*range(1, 10)]
    # X always starts first.
    currentTurn = "X"
    counter = 0
    while True:
        if currentTurn == AI:
            # NOTE: if the AI starts first, it'll always choose index 0 so to save time you could play it.
            cell = FindBestMove(currentGame, AI)
            currentGame[cell - 1] = AI
            currentTurn = player
        elif currentTurn == player:
            PrintBoard(currentGame)
            while True:
                humanInput = int(input("Enter Number: ").strip())
                if humanInput in currentGame:
                    currentGame[humanInput - 1] = player
                    currentTurn = AI
                    break
                else:
                    PrintBoard(currentGame)
                    print("Cell Not Available.")
        if GetWinner(currentGame) != None:
            PrintBoard(currentGame)
            print(f"{GetWinner(currentGame)} WON!!!")
            break
        counter += 1
        if GetWinner(currentGame) == None and counter == 9:
            PrintBoard(currentGame)
            print("Tie.")
            break

if __name__ == "__main__":
    main()