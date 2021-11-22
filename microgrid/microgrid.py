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
            self.players.append(Player(self,i,2))
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
    
    def amnt_SellBuy(self) -> np.array:
        """
        Distributes how much each player selling/buying sells/buy to the microgrid
        """
        i : Player
        amnt_selling = []
        amnt_buying = []
        for i in self.players:
            if i.state == 1:
                amnt_selling.append(i.getCapforSale())
            elif i.state == -1:
                amnt_buying.append(i.getCapToBuy())
            else:
                amnt_selling.append(0)
                amnt_buying.append(0)
        
        amnt_buying = np.array([amnt_buying])
        amnt_selling = np.array([amnt_selling])

        if self.getStorageForSale() > self.getStorageToBuy():
            each_sell = self.getStorageToBuy/np.count_nonzero(amnt_selling)        
            _s = self.getStorageToBuy()
            while amnt_selling[amnt_selling <= each_sell].size != 0:
                _s = _s - np.sum(amnt_selling[amnt_selling <= each_sell])
                each_sell = _s/np.count_nonzero(amnt_selling[amnt_selling > each_sell])
            diff_sell = np.zeros(amnt_selling.shape[0])
            diff_sell[amnt_selling > each_sell] = each_sell
            amnt_selling[amnt_selling > each_sell] = each_sell
        elif self.getStorageForSale() < self.getStorageToBuy:
            each_buy = self.getStorageForSale/np.count_nonzero(amnt_buying)        
            _b = self.getStorageForSale()
            while amnt_buying[amnt_buying <= each_buy].size != 0:
                _b = _b - np.sum(amnt_buying[amnt_buying <= each_buy])
                each_buy = _b/np.count_nonzero(amnt_buying[amnt_buying > each_buy])
            diff_buy = np.zeros(amnt_buying.shape[0])
            diff_buy[amnt_buying > each_buy] = each_buy
            amnt_buying[amnt_buying > each_buy] = each_buy
        else:
            diff_sell = np.zeros(amnt_buying.shape[0])
            diff_buy = np.zeros(amnt_selling.shape[0])
            pass
        amnt_microgrid = amnt_selling - amnt_buying
        amnt_macrogrid = diff_sell - diff_buy 
        return amnt_microgrid, amnt_macrogrid
        
    def getStorageToBuy(self) -> float:
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