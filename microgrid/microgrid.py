from microgrid.player import Player
import numpy as np

class Microgrid():
    AVG = 0.15
    BUY_MAIN = 1
    SELL_MAIN = 0.5
    SELL_MICRO = 0.8
    BUY_MICRO = 0.8
    STORE_BUY = 0
    STORE_SELL = 0
    
    def __init__(self,n):
        self.day = 0
        self.n = n
        self.players = []
        for i in range(n):
            self.players.append(Player(self,i,Player.States.STORING))            

    #tested
    def getStorageForSale(self):
        totalSupply = 0
        i : Player
        for i in self.players:
            sale = i.getCapForSale()
            if sale>0:
                totalSupply += sale
        return totalSupply
    
    def amount_SellBuy(self) -> np.array:
        """
        Distributes how much each player selling/buying sells/buy to the microgrid
        Returns the array of $ transactions for each player
        """
        i : Player
        amnt_selling = []
        amnt_buying = []
        id_selling = []
        id_buying = []
        id_out = []
        for i in self.players:
            if i.state == 1:
                amnt_selling.append(i.getCapForSale())
                id_selling.append(i.id)
            elif i.state == -1:
                amnt_buying.append(i.getCapToBuy())
                id_buying.append(i.id)
            else:
                id_out.append(i.id)

        amnt_buying = np.array(amnt_buying)
        amnt_selling = np.array(amnt_selling)
        diff_buy = np.zeros(amnt_buying.shape[0])
        diff_sell = np.zeros(amnt_selling.shape[0])

        # buy from the players that sell their storage
        if self.getStorageForSale() > self.getStorageToBuy():
            each_sell = self.getStorageToBuy()/np.count_nonzero(amnt_selling)        
            _s = self.getStorageToBuy()
            while amnt_selling[amnt_selling <= each_sell].size != 0:
                _s = _s - np.sum(amnt_selling[amnt_selling <= each_sell])
                each_sell = _s/np.count_nonzero(amnt_selling[amnt_selling > each_sell])
            diff_sell[np.where(amnt_selling > each_sell)] = amnt_selling[np.where(amnt_selling > each_sell)] - each_sell
            amnt_selling[np.where(amnt_selling > each_sell)] = each_sell
        
        elif self.getStorageForSale() < self.getStorageToBuy():
            each_buy = self.getStorageForSale()/np.count_nonzero(amnt_buying)        
            _b = self.getStorageForSale()
            while amnt_buying[amnt_buying <= each_buy].size != 0:
                _b = _b - np.sum(amnt_buying[amnt_buying <= each_buy])
                each_buy = _b/np.count_nonzero(amnt_buying[amnt_buying > each_buy])
            diff_buy[np.where(amnt_buying > each_buy)] = amnt_buying[np.where(amnt_buying > each_buy)] - each_buy
            amnt_buying[np.where(amnt_buying > each_buy)] = each_buy
        else:
            pass

        _aramnt_buying, _ardiff_buy = np.zeros(self.n), np.zeros(self.n)
        _aramnt_buying[id_buying], _ardiff_buy[id_buying] = amnt_buying, diff_buy
        _aramnt_selling, _ardiff_sell = np.zeros(self.n), np.zeros(self.n)
        _aramnt_selling[id_selling], _ardiff_sell[id_selling] = amnt_selling, diff_sell
        total_transac = self.SELL_MICRO*_aramnt_selling + self.SELL_MAIN*_ardiff_sell -\
            self.BUY_MICRO*_aramnt_buying - self.BUY_MAIN*_ardiff_buy
        return total_transac
    
    def amount_gainStorage(self):
        """
        Returns the utility of storaging if overflows, go to main grid
        """
        i: Player
        amnt_storing = []
        amnt_tomaingrid = []
        id_store = []
        for i in self.players:
            if i.state == 0:
                _tostore = i.p-i.c
                _available_storage = i.max_storage - i.b
                if _tostore <= _available_storage:
                    amnt_storing.append(_tostore)
                    amnt_tomaingrid.append(0)
                else:
                    amnt_storing.append(_available_storage)
                    amnt_tomaingrid.append(_tostore - _available_storage)
            else:
                amnt_storing.append(0)
                amnt_tomaingrid.append(0)
        amnt_storing = np.array(amnt_storing)
        amnt_tomaingrid = np.array(amnt_tomaingrid)

        stgain = self.SELL_MICRO #TODO define how this gain will be quantified
        total_utstoring = self.SELL_MAIN*amnt_tomaingrid + stgain*amnt_storing
        return total_utstoring

    #tested
    def getStorageToBuy(self) -> float:
        totalyDamand = np.sum([i.getCapToBuy() for i in self.players])
        return totalyDamand

    def buy(self,amount:float,seller : Player) -> float:
        left = amount
        #if amount cannot be sold fully it not yet possible to sell
        trueDemand = self.getStorageToBuy()
        if trueDemand > 0:
            #can buy the amount
            p : Player
            for p in self.players:
                if p != seller:
                    left = p.buy(left, micro=None)
                    if left == 0:
                        break
        return left #returns amount that is left unsold

    def sell(self,amount:float,buyer : Player) -> float:
        left = amount
        #if amount cannot be sold fully it not yet possible to sell
        trueSupply = self.getStorageForSale()
        if trueSupply > amount:
            #can buy the amount
            p : Player
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
