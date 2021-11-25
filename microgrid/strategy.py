import numpy as np
class Strategy:
    def __init__(self,choice:int):
        self.choice = choice
    def _alwaysBuy():
        pass
    def _alwaysSell():
        pass
    

    def utility(self,s,grid):
        """
            x - amount to buy,sell
            s - 0, buy 1,sell
            grid - grid
        """
        if self.choice == self.Choice.ALWAYS_BUY:
            return 
        elif self.choice == self.Choice.ALWAYS_SELL:
            return
        else:
            SELLING = 0
            BUYING = 1
            STORAGE = 2
            table = np.array([
                        #buy,sell
                        [1,0.5],#Main
                        [0.8,0.8],#Micro
                        [0,0]])#Storage
            if SELLING in s:
                #find biggest
                subtable = table[:,1].flatten()
                location = np.argwhere(subtable == np.amax(subtable))[0].flatten()
                #returns a dict: a - strategy b - with whom to apply strategy
                return {SELLING: location}
            if BUYING in s:
                #find smallest
                subtable = table[:,0].flatten()
                subtable[-1] = np.Inf # cannot buy from storage
                location = np.argwhere(subtable == np.amin(subtable))[0].flatten()
                return {BUYING: location}

    """
    def _comb_strategies(self,m:Microgrid):
       
        Combinatorics of all possible strategies players can play
       
        i:Player
        space_strategies = []
        for i in m.players:
            space_strategies.append(i.possible_strategies())

        space_strategies = list(itertools.product(*space_strategies))
        return space_strategies
    """
    """
    def _utility_function(self,m:Microgrid, strategy):
    
        Returns the utility
        1D - Value depends on player state
        utility = 1D.[$Sell $Buy $Store]
     
        i:Player
        for i in m.players:
            # set the strategy for the player i
            i.state = strategy[i.id]
        total_transac = m.amount_SellBuy()
        gain_storage = m.amount_gainStorage()
        utility = total_transac + gain_storage
        return utility
    """
    """
    def _strategies_utilities(self,m:Microgrid):
  
        Computes utilities of each set of strategies
      
        space_strategies = self._comb_strategies(m)
        calc_utilities = []
        for s in space_strategies:
            calc_utilities.append(self._utility_function(m,s))
        return np.array(calc_utilities)
    """
    class Choice:
        GT = 0
        ALWAYS_BUY = 1
        ALWAYS_SELL = 2