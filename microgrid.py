from player import Player
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

    def getStorageForSale(self):
        totalStorage = 0
        i : Player
        for i in self.players:
            sale = i.getCapForSale()
            if sale>0:
                totalStorage += sale
        return totalStorage

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

    def buy(self,amount : Player):
        trueTotal = self.getStorageForSale() - amount.getCapForSale()
        #TODO self only to other people that
        #amountEach = amount/nPlayerBuying
        for i in nPlayersbuying:
            i.buy(amountEach)
        # microgrid sells to players that want to buy    
        if (self.getStorageForSale() - amount) < 0:
            return True
        #TODO finish method
    #def currentPrice(self):
    #    return np.interp(self.t,[0,24],[self.OFF_PEEK,self.PEEK])
    
    def step(self):
        self.d += 1
        """
        for i in self.players:
            i.step()
        """