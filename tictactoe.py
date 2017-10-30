"""
Playable Tic-Tac-Toe game with unbeatable A.I.
A.I. based on MiniMax game tree with alpha beta pruning
By Jonathan Yu 30/10/17
"""


import numpy as np


def InitGrid():
    """initialise grid"""
    return np.zeros([3,3])


class Game:
    """Game"""
    #initialise game variables
    state = InitGrid() #0:free; 1:player; 2:ai
    over = False #when gameover: over=True
    playerTurn = 'player' #player: human player; ai: A.I. player
    playerKey = {0:"-", 1:"X", 2:"O"}
    winStates = [np.array([[1,1,1],[0,0,0],[0,0,0]]),
                 np.array([[0,0,0],[1,1,1],[0,0,0]]),
                 np.array([[0,0,0],[0,0,0],[1,1,1]]),
                 np.array([[1,0,0],[1,0,0],[1,0,0]]),
                 np.array([[0,1,0],[0,1,0],[0,1,0]]),
                 np.array([[0,0,1],[0,0,1],[0,0,1]]),
                 np.array([[1,0,0],[0,1,0],[0,0,1]]),
                 np.array([[0,0,1],[0,1,0],[1,0,0]])]


    def UpdateGame(self, next_state):
        """update game with next state, prints game state"""
        #update states, print new grid
        self.state = next_state
        self.PrintGrid()
        #update playerTurn
        if self.playerTurn == 'player':
            self.playerTurn = 'ai'
        else:
            self.playerTurn = 'player'
        #check status
        next_status = self.CheckState(next_state)
        if next_status > 0:
            self.over = True
            if next_status == 1:
                #win
                print 'player WON!'
            elif next_status == 2:
                #win
                print 'ai WON!'
            elif next_status == 3:
                #draw
                print 'DRAW!'


    def ValidMove(self, move):
        """check if a move is valid - move=(x,y)"""
        if self.state[move] == 0:
            return True
        else:
            return False


    def ListPossibleStates(self, current_state, player):
        """list all possible next states for current player"""
        possibleStates = []
        if player == 'player':
            playerVal = 1 #1:player; 2:ai
        else:
            playerVal = 2 #1:player; 2:ai
        (M,N) = self.state.shape
        for m in range(M):
            for n in range(N):
                move = (m,n)
                if current_state[move] == 0:
                    tmp_state = np.copy(current_state)
                    tmp_state[move] = playerVal
                    possibleStates.append(tmp_state)
        return possibleStates


    def CheckState(self, state):
        """check game state for win or draw
            return values:
                0: game not over
                1: game over: player or ai won
                2: game over: draw
        """
        for mask in self.winStates:
            if np.array_equal(state*mask,mask):
                #player 1 won
                return 1
            elif np.array_equal(state*mask,mask*2):
                #player 2 (ai) won
                return 2
        #check for draw
        draw = not np.any(state==0)
        if draw:
            #draw
            return 3
        else:
            #not game over
            return 0


    def PrintGrid(self):
        """print current game state (tictactoe grid)"""
        M,N = self.state.shape
        for r in range(M):
            row = ""
            for c in range(N):
                row = row + self.playerKey[self.state[r,c]] + " "
            print row


    def MiniMax(self, current_state, player, depth):
        """recursive minimax function"""
        next_states = self.ListPossibleStates(current_state, player)
        #check current status
        status = self.CheckState(current_state)
        #terminal node reached - return minimax score
        if len(next_states) == 0 or status > 0:
            #calculate minimax score
            if status == 1:
                #player wins
                return 10-depth
            elif status == 2:
                #player loses (ai wins)
                return -10+depth
            else:
                #draw
                return 0
        scores = []
        #if player
        if player == 'player':
            for state in next_states:
                scores.append(self.MiniMax(state, 'ai', depth+1))
            return max(scores)
        #if ai
        else:
            for state in next_states:
                scores.append(self.MiniMax(state, 'player', depth+1))
            return min(scores)


    def MiniMaxChoice(self, current_state, player):
        """choose next move based on minimax value"""
        next_states = self.ListPossibleStates(current_state, player)
        if len(next_states) == 0:
            print "Error: MiniMaxChoice()"
        maxScore = -99
        minScore = 99
        for state in next_states:
            if player == 'player':
                score = self.MiniMax(state, 'ai', 0)
                #print state, score, player
                if score > maxScore:
                    #update maxScore and nextState
                    maxScore = score
                    nextState = state
            #player is ai
            elif player == 'ai':
                score = self.MiniMax(state, 'player', 0)
                #print state, score, player
                if score < minScore:
                    #update minScore and nextState
                    minScore = score
                    nextState = state
        return nextState


    def AlphaBeta(self, current_state, player, alpha, beta, depth):
        """recursive alphabeta function"""
        next_states = self.ListPossibleStates(current_state, player)
        #check current status
        status = self.CheckState(current_state)
        #terminal node reached - return minimax score
        if len(next_states) == 0 or status > 0:
            #calculate minimax score
            if status == 1:
                #player wins
                return 10-depth
            elif status == 2:
                #player loses (ai wins)
                return -10+depth
            else:
                #draw
                return 0
            scores = []
        #if player
        if player == 'player':
            v = -999 #max for immediate children
            for state in next_states:
                score = self.AlphaBeta(state, 'ai', alpha, beta, depth+1)
                v = max(v, score)
                if v >= beta: return v #alpha cutoff
                else: alpha = max(alpha, v)
            return v
        #if ai
        else:
            v = 999
            for state in next_states:
                score = self.AlphaBeta(state, 'player', alpha, beta, depth+1)
                v = min(v, score)
                if v <= alpha: return v #beta cutoff
                else: beta = min(beta, v)
            return v


    def AlphaBetaChoice(self, current_state, player):
        """choose next move based on alphabeta value"""
        next_states = self.ListPossibleStates(current_state, player)
        if len(next_states) == 0:
            print "Error: AlphaBetaChoice()"
        maxScore = -999
        minScore = 999
        for state in next_states:
            if player == 'player':
                score = self.AlphaBeta(state, 'ai', -999, 999, 0)
                #print state, score, player
                if score > maxScore:
                    #update maxScore and nextState
                    maxScore = score
                    nextState = state
            #player is ai
            elif player == 'ai':
                score = self.AlphaBeta(state, 'player', -999, 999, 0)
                #print state, score, player
                if score < minScore:
                    #update minScore and nextState
                    minScore = score
                    nextState = state
        return nextState


def main():
    """main function"""
    g = Game()
    g.PrintGrid()
    while(g.over != True):
        if g.playerTurn == 'player':
            #player
            in_data = raw_input('Player make a move: <row> <col>').split()
            row = int(in_data[0])
            col = int(in_data[1])
            move = (row,col)
            if not g.ValidMove(move):
                print "Error: Invalid move... idiot"
                g.PrintGrid()
                continue
            next_state = g.state
            next_state[(row,col)] = 1
        else:
            #AI
            print "AI making move..."
            next_state = g.AlphaBetaChoice(g.state, 'ai')
        g.UpdateGame(next_state)


"""if file directly opened: run main()"""
if __name__ == "__main__": main()
