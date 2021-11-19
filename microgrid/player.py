from random import random

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
        self.grid = grid # Microgrid object
        self.id = id
        self.p=p*random()
        self.c=c*random()
        self.b=b*random()
        self.selling = 0
        self.buying = 0
        self.produced = False
    
    def __eq__(self,other):
        return self.id == other.id
    def __ne__(self,other):
        return self.id != other.id
    
    def getCapForSale(self) -> float:
        return self.selling
    def _updateCapForSale(self):
        #more logic here
        remaining = self.b + self.p-self.c - self.blackout
        if remaining > 0:
            self.selling = abs(remaining)
        else:
            self.selling = 0
    def getCapToBuy(self) -> float:
        return self.buying
    def _updateCapToBuy(self):
        #more logic here
        remaining = self.b + self.p-self.c - self.blackout
        if remaining < 0:
            self.buying = abs(remaining)
        else:
            self.buying = 0
    
    def _updateStorage(self,amount:float) -> None:
        """
        Updates the storage and returns the amount of enery that was not used to
        charge the battery
        """
        toBeStorage = self.b + amount
        if toBeStorage >= self.max_storage:
            self.b = self.max_storage
            return toBeStorage-self.max_storage
            #return excess capacity
        else:
            self.b += amount
            return 0
    def sell(self,amount: float,micro: bool) -> float:
        pass
    def buy(self,amount:float,micro: bool) -> float:
        pass

    def step(self):
        #update sell
        self._updateCapToBuy()
        self._updateCapForSale()
        pass # update battery values
    #TODO make players know forcast for next hour 
    #TODO current decision on the current hour
