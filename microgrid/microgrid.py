from microgrid.player import Player
import numpy as np

class Microgrid():
    AVG = 0.15
    BUY_MAIN = 1
    SELL_MAIN = 0.5
    SELL_MICRO = 0.8
    BUY_MICRO = 0.8

    def __init__(self,n):
        self.day = 0
        self.n = n
        self.players = []
        for i in range(n):
            self.players.append(Player(self,i))
        for i in self.players:
            i.step()

    def getStorageForSale(self):
        totalSupply = 0
        i : Player
        for i in self.players:
            sale = i.getCapForSale()
            if sale>0:
                totalSupply += sale
        return totalSupply
    def getStorageToBuy(self):
        totalyDamand = 0
        i : Player
        for i in self.players:
            damand = i.getCapToBuy()
            if damand>0:
                totalyDamand += damand
        return totalyDamand

    def getTotalP(self):
        p = 0
        i : Player
        for i in self.players:
            pi = i.p
            if pi>0:
                p += pi
        return p
    def getTotalC(self):
        c = 0
        i : Player
        for i in self.players:
            ci = i.c
            if ci>0:
                c += ci
        return c

    def buy(self,amount:float) -> float:
        pass

    def sell(self,amount:float) -> float:
        pass

    def step(self) -> None:
        self.day += 1
        for i in self.players:
            i.step()