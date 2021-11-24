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
        """
        State: 0 - Selling, 1 - Buying, 2- Storage, 3 - do nothing
        """
        #update state here
        self.state = state
        self.selling = 0
        self.buying = 0
        self.unused = 0
        self.step()

    #tested
    def __eq__(self,other):
        return self.id == other.id
    def __ne__(self,other):
        return self.id != other.id
    
    def possible_strategies(self) -> list:
        """
        Possible strategy player can follow depending on available energy
        """
        if self.getCapToBuy() > 0:
            strategies = [self.States.BUYING] # Buy
        elif self.getCapForSale() > 0:
            strategies = [self.States.SELLING,self.States.STORING] #Sell or Store
        return strategies

    #tested
    def getCapForSale(self) -> float:
        """
        Get the amount that can be sold (including battery)
        """
        if self.selling > 0:
            return self.selling
        return 0
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
        self.buying = 0
        diff = self.c - self.p
        if diff <= 0:
            self.buying = 0
        else:
            self.buying = diff + self.getAvailableStorage()
        return self.buying
    #tested
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
    #tested
    def getAvailableStorage(self) -> float:
        """
        Get the available storage
        """
        r = self.b - self.blackout
        if r <= 0:
            return 0
        return r
    
    #tested -> might need more testing
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

    #tested
    def step(self):
        #update sell
        #TODO production should change depending on a day
        self.unused = self.p - self.c
        #charge battery if unused (model should check this out )
        self.unused = self._updateStorage(self.unused)
        self._updateCapToBuy()
        self._updateCapForSale()
        
    class States:
        SELLING = 0
        BUYING = 1
        STORING = 2
        DO_NOTHING = 3