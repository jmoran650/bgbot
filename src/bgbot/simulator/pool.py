from bgbot.simulator.minion import Tribe

'''
tier 1 : 15 copies
tier 2 : 15 copies
tier 3 : 13 copies
tier 4 : 11 copies
tier 5 : 9 copies
tier 6 : 7 copies

'''

class Pool(list[Tribe]):

    def __init__(tribes):
        self.pool = []
        for tribe in tribes:


            {tribe, tier : minion, count }

            roll(optionally=tribe, tier, number of cards):
                
                add minions currently in shop back to pool by incrementing counter for each one. counter should never go above number of copies of minion for that tier

                if not tribe:
                    retrieve number of cards that are of tier or below, decrementing count of each one
                if tribe retrieve number of cards that are of tier or below and of tribe, decrementing count of each one)

    def discover(self, tribe=optional, tier=optional, number of cards=optional):
        