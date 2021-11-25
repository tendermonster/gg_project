import numpy as np


class Strategy:
    def __init__(self, choice: int):
        self.choice = choice

    def _alwaysBuy():
        pass

    def _alwaysSell():
        pass

    def utility(self, s, grid):
        """
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
            table = np.array(
                [
                    # buy,sell
                    [1, 0.5],  # Main
                    [0.8, 0.8],  # Micro
                    [0, 0],
                ]
            )  # Storage
            if SELLING in s:
                # find biggest
                subtable = table[:, 1].flatten()
                location = np.argwhere(subtable == np.amax(subtable))[0].flatten()
                # returns a dict: a - strategy b - with whom to apply strategy
                return {SELLING: location}
            if BUYING in s:
                # find smallest
                subtable = table[:, 0].flatten()
                subtable[-1] = np.Inf  # cannot buy from storage
                location = np.argwhere(subtable == np.amin(subtable))[0].flatten()
                return {BUYING: location}

    class Choice:
        GT = 0
        ALWAYS_BUY = 1
        ALWAYS_SELL = 2
