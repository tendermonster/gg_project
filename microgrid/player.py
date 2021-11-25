from microgrid.strategy import Strategy
import random

class Player():
    """
        per day 
        max storage is 100
        max consumption is 100
        max production is 100
    """
    blackout = 20
    max_storage = 150
    #tested
    def __init__(self,grid,id,state,p=100,c=100,b=100,randomize=True):
        random.seed(id)
        self.money = 1000
        self.grid = grid # Microgrid object
        self.id = id
        if randomize:
            self.p=p*random.random()
            self.c=c*random.random()
            self.b=b*random.random()  
        else:
            self.p=p
            self.c=c
            self.b=b
        self.strategy = Strategy(Strategy.Choice.GT)
        """
        State: 0 - Selling, 1 - Buying, 2- Storage, 3 - do nothing
        """
        #update state here
        self.state = state
        self.selling = 0
        self.buying = 0
        self.unused = 0
        self.update_parameters()

    #tested
    def __eq__(self,other):
        return self.id == other.id
    def __ne__(self,other):
        return self.id != other.id
    #change strategy
    def setStrategy(self,strategy : Strategy):
        self.strategy = strategy

    #tested
    def getCapForSale(self) -> float:
        """
        Get the amount that can be sold (including battery)
        """
        return self.selling
    #tested
    def _updateCapForSale(self):
        #more logic here
        self.selling = 0
        remaining = self.b - self.blackout
        if remaining > 0:
            self.selling = remaining
        if self.unused > 0:
            self.selling += self.unused
            self.unused = 0
    #tested
    def getCapToBuy(self) -> float:
        """
        Get the amount needed to buy (including using battery)
        """
        return self.buying
    #tested
    def _updateCapToBuy(self):
        self.buying = 0
        remaining = self.getAvailableStorage()
        if remaining < 0:
            self.buying = abs(remaining)
        if self.unused < 0:
            self.buying += abs(self.unused)
            self.unused = 0
    #tested
    def getAvailableStorage(self) -> float:
        """
        Get the available storage
        """
        return self.b - self.blackout
    
    #tested -> might need more testing
    def _updateStorage(self,amount:float) -> None:
        """
        Updates the storage and returns the amount of enery that was not used to
        charge the battery
        """
        # discharging if capacity is available
        if amount < 0:
            diff = (self.b-abs(amount))
            if diff<0:
                self.b = 0 # discharged to 0%
                return diff
            else:
                self.b = diff
                return 0

        #charging
        toBeStorage = self.b + amount
        if toBeStorage >= self.max_storage:
            self.b = self.max_storage
            return toBeStorage-self.max_storage
            #return excess capacity
        else:
            self.b = toBeStorage
            return 0

    def possible_strategies(self) -> list:
        """
        Possible strategy player can follow depending on available energy
        """
        strategies = []
        if self.getCapToBuy() > 0:
            return [self.States.BUYING] # Buy
        elif self.getCapForSale() > 0:
            strategies = [self.States.SELLING,self.States.STORING] #Sell or Store
        return strategies

    def sell(self,amount: float,micro: bool) -> float:
        left = amount
        #purchase is done from microgrid itself
        if micro is None:
            #sold everything
            if amount < self.getCapForSale():
                self._updateStorage(-amount)
                self._updateCapForSale()
                return 0
            return left
            
        left = amount
        if micro:
            left = self.grid.buy(amount,self) #buy from grid
            sold = amount - left
            self.money += sold*self.grid.AVG*self.grid.SELL_MICRO
        #sell to grid the rest
        self.money += left*self.grid.AVG*self.grid.SELL_MAIN
        #might be needed here
        self._updateStorage(-amount)
        self._updateCapForSale()
        self._updateCapToBuy()

    def buy(self,amount:float,micro: bool) -> float:
        #in this case the amount will be bought fully
        #for now buy only to charge the battery
        left = amount
        if micro is None:
            #partial buy
            if amount > self.getCapToBuy():
                left = amount - self.getCapToBuy()
                self._updateStorage(self.getCapToBuy())
                self._updateCapForSale()
                self._updateCapToBuy()
                return left
            #buy all
            if amount <= self.getCapToBuy():
                self._updateStorage(amount)
                self._updateCapForSale()
                self._updateCapToBuy()
                return 0
            return left

        if micro:
            left = self.grid.sell(amount,self) #buy from grid
            bought = amount - left
            self.money -= bought*self.grid.AVG*self.grid.BUY_MICRO
        #buy from main grid
        self.money -= left*self.grid.AVG*self.grid.BUY_MAIN
        unused = self._updateStorage(amount)
        #sell to grid unused
        #TODO CONNECT MODEL HERE
        self.money += unused*self.grid.AVG*self.grid.BUY_MAIN
        #might be needed here
        self._updateCapToBuy()
        self._updateCapForSale()

    def _apply_strategy(self,s):
        buying = self.States.BUYING
        selling = self.States.SELLING
        if buying in s:
            #buy
            if s[buying] == self.States.MAIN_GRID:
                self.buy(amount=self.getCapToBuy(),micro=False)
            elif s[buying] == self.States.MICRO_GRID:
                self.buy(amount=self.getCapToBuy(),micro=True)
            else:
                #storing
                pass
        elif selling in s:
            #selling
            if s[selling] == self.States.MAIN_GRID:
                self.sell(amount=self.getCapForSale(),micro=False)
            elif s[selling] == self.States.MICRO_GRID:
                self.sell(amount=self.getCapForSale(),micro=True)
            else:
                #storing
                pass
    def update_parameters(self):
        # update buy sell parameters
        if self.p == 0 and self.c == 0:
            self.p=100*random.random()
            self.c=100*random.random() 
        self.unused = self.p - self.c
        self.p,self.c = 0,0 # maybe do not delete but 
        self.unused = self._updateStorage(self.unused)
        self._updateCapToBuy()
        self._updateCapForSale()

    #tested
    def step(self):
        #update sell
        #TODO production should change depending on a day
        #decide on the strategy
        if self.grid is not None:
            s = self.possible_strategies()
            bestStrategy = self.strategy.utility(s,self.grid)
            if len(s) != 0:
                #only do if some actions are needed
                self._apply_strategy(bestStrategy)
        self.update_parameters()
        
    class States:
        SELLING = 0
        BUYING = 1
        STORING = 2
        DO_NOTHING = 3
        MAIN_GRID = 0
        MICRO_GRID = 1
        STORAGE = 2