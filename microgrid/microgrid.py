from microgrid.player import Player
from microgrid.strategy import Strategy
import random
import views
import numpy as np


class Microgrid:
    AVG = 0.15
    BUY_MAIN = 1
    SELL_MAIN = 0.5
    SELL_MICRO = 0.8
    BUY_MICRO = 0.8
    STORE_BUY = 0
    STORE_SELL = 0

    def __init__(self, n, strategy: Strategy, randomize = True):
        self.day = 0
        self.n = n
        self.players = []
        if strategy is None:
            for i in range(n):
                random_s = np.round(np.random.uniform(0, 2))
                strategy = Strategy(choice=random_s)
                random.seed(i)
                if randomize == False:
                    p, c, b = 100* random.random(), 100* random.random(), 100* random.random()
                
                self.players.append(
                    Player(self, i, state=Player.States.STORING, strategy=strategy,
                    p=p,c=c, b=b, randomize=randomize)
                )
        else:
            for i in range(n):
                random.seed(i)
                if randomize == False:
                    p, c, b = 100* random.random(), 100* random.random(), 100* random.random()
                
                self.players.append(
                    Player(self, i, state=Player.States.STORING, strategy=strategy,
                    p=p,c=c, b=b, randomize=randomize)
                )

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

    def step(self) -> dict:
        self.day += 1
        step_series = views.create_series()
        for i in self.players:
            i.update_parameters()
            i.bought = 0
            i.sold = 0
            i.bought_main = 0
            i.sold_main = 0
        for i in self.players:
            for k in step_series:
                player_series = i.step()
                step_series[k] = np.append(step_series[k], player_series[k])
        return step_series
