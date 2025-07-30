# pylint: skip-file 
# pyright: reportMissingImports=false, reportUnknownMemberType=false, reportSyntaxError=false
def class Combat(Player1, Player2):

    board1 = Player1.board
    board2 = Player2.board

    def determineOrder(board1, board2):
        if (board1.numberOfMinions > board2.numberOfMinions):
            Combat.startCombat(board1, board2, rand=false)
        else if (board1.numberOfMinions < board2.numberOfMinions):
            Combat.startCombat(board2, board1, rand=false)
        else if (board1.numberOfMinions == board2.numberOfMinions):
            Combat.startCombat(board1, board2, rand=true)
    
    def startCombat(board1, board2, rand):
        if rand = true:
            coinflip to determine who goes first
        else:
            for minions in board1, board2:
                # This needs to be in the order they attack, needs to trigger hero start of combats as well
                combat.performStartOfCombat(board1, board2)
    
    def performStartOfCombat(board1, board2, order):
        for minions in board1, board2 according to order:
            minion.executeStartOfCombat()
    
    def PerformCombat(board1, board2, order):
        while minions are still alive on both boards:
            for minions in board1, board2:
                minion.attack()

        when all minions are dead for a player:
            damageTaken = calculateDamage(winningBoard)
            losingPlayer.takeDamage(damageTaken)

    

