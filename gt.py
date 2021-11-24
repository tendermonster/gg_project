from microgrid.microgrid import Microgrid
from microgrid.player import Player
import numpy as np
import itertools

def comb_strategies (m:Microgrid):
    """
    Combinatorics of all possible strategies players can play
    """
    i:Player
    space_strategies = []
    for i in m.players:
        space_strategies.append(i.possible_strategies())

    space_strategies = list(itertools.product(*space_strategies))
    return space_strategies

def utility_function(m:Microgrid, strategy):
    """
    Returns the utility
    1D - Value depends on player state
    utility = 1D.[$Sell $Buy $Store]
    """
    i:Player
    for i in m.players:
        i.state = strategy[i.id]
    total_transac = m.amnt_SellBuy()
    gain_storage = m.amnt_gainStorage()
    utility = total_transac + gain_storage
    return utility

def strategies_utilities(m:Microgrid):
    """
    Computes utilities of each set of strategies
    """
    space_strategies = comb_strategies(m)
    calc_utilities = []
    for s in space_strategies:
        calc_utilities.append(utility_function(m,s))
    return np.array(calc_utilities)

def find_NE(m:Microgrid):
    """
    Finds Nash Equilibrium of the game (Fictional playing? Explore more algorithms)
    """

def max_TotalWelfare(m:Microgrid):
    """
    Finds the set of strategy with the maximum total Welfare
    """