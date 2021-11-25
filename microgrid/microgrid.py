from microgrid.player import Player
import numpy as np


class Microgrid:
    AVG = 0.15
    BUY_MAIN = 1
    SELL_MAIN = 0.5
    SELL_MICRO = 0.8
    BUY_MICRO = 0.8
    STORE_BUY = 0
    STORE_SELL = 0

    def __init__(self, n):
        self.day = 0
        self.n = n
        self.players = []
        for i in range(n):
            self.players.append(Player(self, i, Player.States.STORING))

    # tested
    def getStorageForSale(self):
        totalSupply = 0
        i: Player
        for i in self.players:
            sale = i.getCapForSale()
            if sale > 0:
                totalSupply += sale
        return totalSupply

    # tested
    def getStorageToBuy(self) -> float:
        totalyDamand = np.sum([i.getCapToBuy() for i in self.players])
        return totalyDamand

    def buy(self, amount: float, seller: Player) -> float:
        left = amount
        # if amount cannot be sold fully it not yet possible to sell
        trueDemand = self.getStorageToBuy()
        if trueDemand > 0:
            # can buy the amount
            p: Player
            for p in self.players:
                if p != seller:
                    left = p.buy(left, micro=None)
                    if left == 0:
                        break
        return left  # returns amount that is left unsold

    def sell(self, amount: float, buyer: Player) -> float:
        left = amount
        # if amount cannot be sold fully it not yet possible to sell
        trueSupply = self.getStorageForSale()
        if trueSupply > amount:
            # can buy the amount
            p: Player
            for p in self.players:
                if p != buyer:
                    left = p.sell(left, micro=None)
                    if left == 0:
                        break
        return left

    def step(self) -> None:
        self.day += 1
        for i in self.players:
            i.update_parameters()
        for i in self.players:
            i.step()
