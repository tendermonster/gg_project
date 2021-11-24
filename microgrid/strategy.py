from microgrid.microgrid import Microgrid
from microgrid.player import Player
import numpy as np
import itertools

class Strategy:
    def __init__(self,choice:int):
        self.choice = choice
    def _alwaysBuy():
        pass
    def _alwaysSell():
        pass
    def _comb_strategies(self,m:Microgrid):
        """
        Combinatorics of all possible strategies players can play
        """
        i:Player
        space_strategies = []
        for i in m.players:
            space_strategies.append(i.possible_strategies())

        space_strategies = list(itertools.product(*space_strategies))
        return space_strategies

    def _utility_function(self,m:Microgrid, strategy):
        """
        Returns the utility
        1D - Value depends on player state
        utility = 1D.[$Sell $Buy $Store]
        """
        i:Player
        for i in m.players:
            # set the strategy for the player i
            i.state = strategy[i.id]
        total_transac = m.amount_SellBuy()
        gain_storage = m.amount_gainStorage()
        utility = total_transac + gain_storage
        return utility

    def _strategies_utilities(self,m:Microgrid):
        """
        Computes utilities of each set of strategies
        """
        space_strategies = self._comb_strategies(m)
        calc_utilities = []
        for s in space_strategies:
            calc_utilities.append(self._utility_function(m,s))
        return np.array(calc_utilities)
    
    def utility(self):
        pass

    def find_NE(m:Microgrid):
        """
        Finds Nash Equilibrium of the game (Fictional playing? Explore more algorithms)
        """

    def max_TotalWelfare(m:Microgrid):
        """
        Finds the set of strategy with the maximum total Welfare
        """
    class Choice:
        GT = 0
        ALWAYS_BUY = 1
        ALWAYS_SELL = 2