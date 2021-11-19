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
    #TODO implement utility variable
    def __init__(self,grid,id,p=100,c=100,b=100):
        random.seed(id)
        self.grid = grid # Microgrid object
        self.id = id
        self.p=p*random.random()
        self.c=c*random.random()
        self.b=b*random.random()
        self.selling = 0
        self.buying = 0
        self.unused = 0
        self.produced = False
    
    def __eq__(self,other):
        return self.id == other.id
    def __ne__(self,other):
        return self.id != other.id
    
    def getCapForSale(self) -> float:
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
        return self.buying
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
        if micro:
            unsold = self.grid.buy(amount)
            self.selling = unsold 
        else:
            #sell to main grid
            self.selling = 0
    def buy(self,amount:float,micro: bool) -> float:
        pass

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
