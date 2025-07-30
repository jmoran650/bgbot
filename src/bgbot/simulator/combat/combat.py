# pylint: skip-file 
# pyright: reportMissingImports=false, reportUnknownMemberType=false, reportSyntaxError=false
def class Combat(Player1, Player2):

    board1 = Player1.board
    board2 = Player2.board

    def determineOrder(board1, board2):
        if (board1.numberOfMinions > board2.numberOfMinions):
            return "board1 goes first"
        else if (board1.numberOfMinions < board2.numberOfMinions):
            return "board2 goes first"
        else if (board1.numberOfMinions == board2.numberOfMinions):
            return coinflip, heads = board1 goes first, tails = board2 goes first
        
    
    def startOfCombat(board1, board2, order):
        if order = "board1 goes first":
            combat.performStartOfCombat(board1)
            combat.performStartOfCombat(board2)
        else if order = "board2 goes first":
            combat.performStartOfCombat(board2)
            combat.performStartOfCombat(board1)
    
    def performStartOfCombat(board):
        for minions in board:
            minion.executeStartOfCombat()
    
    def PerformCombat(board1, board2):
        while minions are still alive on both boards:
            for minions in board1, board2:
                minion.attack()

        damageTaken = calculateDamage(winningBoard)
        losingPlayer.takeDamage(damageTaken)
        returnToShopPhase()

    

