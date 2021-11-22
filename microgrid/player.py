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
    def __init__(self,grid,id,state,p=100,c=100,b=100):
        random.seed(id)
        self.money = 1000
        self.grid = grid # Microgrid object
        self.id = id
        self.p=p*random.random()
        self.c=c*random.random()
        self.b=b*random.random()
        """
        State: 1 - Selling, -1 - Buying, 0 - Storage, 2 - do nothing
        """
        self.state = state
        self.selling = 0
        self.buying = 0
        self.unused = 0
        self.produced = False

    def __eq__(self,other):
        return self.id == other.id
    def __ne__(self,other):
        return self.id != other.id

    def possible_strategies(self) -> list:
        """
        Possible strategy player can follow depending on available energy
        """
        if ((self.getCapToBuy > 0)):
            pstrategies = [-1] # Buy
        elif ((self.getCapForSale > 0)&(self.b + self.getCapForSale > self.max_storage)):
            pstrategies = [1] #Sell
        elif (self.getCapForSale > 0):
            pstrategies = [1,0] #Sell or Store
        return pstrategies

    def getCapForSale(self) -> float:
        """
        Get the amount that can be sold (including battery)
        """
        self.selling = 0 if self.p - self.c <= 0 else self.p - self.c + self.getAvStor()
        return self.selling

    def _updateCapForSale(self):
        #more logic here
        self.selling = 0
        remaining = self.b - self.blackout
        if remaining > 0:
            self.selling = remaining
        if self.unused > 0:
            self.selling += self.unused
            self.unused = 0

    def getCapToBuy(self) -> float:
        """
        Get the amount needed to buy (including using battery)
        """
        self.buying = 0 if self.c - self.p <= 0 else self.c - self.p - self.getAvStor()
        return self.buying

    def getAvStor(self) -> float:
        """
        Get the available storage
        """
        return 0 if self.b - self.blackout <= 0 else self.b - self.blackout

    def _updateCapToBuy(self):
        #model logic calls here
        self.buying = 0
        remaining = self.b - self.blackout
        if remaining < 0:
            #need to be charge
            self.buying = abs(remaining)
            #charge after buying ??? 
            # call buying function here ????
        if self.unused < 0:
            self.buying += abs(self.unused)
            self.unused = 0
            #buy directly here ??? 
            # or wait for microgrid to sell first ?????
            #gt plz help
    
    def _updateStorage(self,amount:float) -> None:
        """
        Updates the storage and returns the amount of enery that was not used to
        charge the battery
        """
        # discharging
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

    def sell(self,amount: float,micro: bool) -> float:
        #TODO CONNECT MODEL HERE
        #THIS IS JUST A DEMO LOGIC
        if self.selling >= amount:
            #handle the exceptions
            raise Exception("cannot sell this much")
        #in this case the amount will be sold fully
        left = amount
        if micro:
            left = self.grid.buy(amount) #buy from grid
            sold = amount - left
            self.money += sold*self.grid.AVG*self.grid.SELL_MICRO
        #sell to grid the rest
        self.money += left*self.grid.AVG*self.grid.SELL_MAIN
        #might be needed here
        self.selling = 0 # sold everything
        self._updateCapToBuy()

    def buy(self,amount:float,micro: bool) -> float:
        #TODO CONNECT MODEL HERE
        #THIS IS JUST A DEMO LOGIC
        if self.buying <= amount:
            #handle the exceptions 
            raise Exception("sorry i cannot buy this much")

        #in this case the amount will be bought fully
        #for now buy only to charge the battery
        left = amount
        if micro:
            left = self.grid.sell(amount) #buy from grid
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

    def step(self):
        #update sell
        #TODO production should change depending on a day
        self.unused = self.p - self.c
        #charge battery if unused (model should check this out )
        self.unused = self._updateStorage(self.unused)
        self._updateCapToBuy()
        self._updateCapForSale()
        
        pass # update battery values
    #TODO make players know forcast for next hour 
    #TODO current decision on the current hour
