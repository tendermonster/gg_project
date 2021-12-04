import numpy as np


class Strategy:
    def __init__(self, choice: int):
        self.choice = choice

    def _chooseoptimum(self,s,table:np.array):
        SELLING = 0
        STORING = 2
        BUYING = 1
        if SELLING in s and STORING in s: # only happens if choice = GT
            # find biggest
            subtable = table[:, 1].flatten()
            location = np.argwhere(subtable == np.amax(subtable))[0].flatten()
            if location == 2:
                return {STORING: location}
            else:
                # returns a dict: a - strategy b - with whom to apply strategy 
                return {SELLING: location}    
        
        if SELLING in s:
            # find biggest
            subtable = table[0:2, 1].flatten() # No storage
            location = np.argwhere(subtable == np.amax(subtable))[0].flatten()
            return {SELLING: location}
        
        if BUYING in s:
            # find smallest
            subtable = table[0:2, 0].flatten() # No Storage
            subtable[-1] = np.Inf  # cannot buy from storage
            location = np.argwhere(subtable == np.amin(subtable))[0].flatten()
            return {BUYING: location}

    def utility(self, s, grid):
        """
        s - 0, buy 1,sell
        grid - grid
        """
        table = np.array(
            [
            # buy #sell
            [1, 0.5],  # Main
            [0.8, 0.8],  # Micro
            [0, 0] # Storage
            ])
        return self._chooseoptimum(s, table)

    class Choice:
        GT = 0
        ALWAYS_BUY = 1
        ALWAYS_SELL = 2
