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
    def __init__(self,grid,id,p=100,c=100,st=100):
        self.grid = grid # Microgrid object
        self.id = id
        self.p=p*random()
        self.c=c*random()
        self.st=st*random()
    
    def getCapForSale(self):
        total = self.st+(self.p-self.c-self.blackout)
        if total >= self.max_storage:
            return self.max_storage
        return total

    def sell(self,mode: bool):
        """
        Args:
            mode (int): True if selling to microgrid, false if sell to Maingrid
        #sellf all available ?"""
        amount = self.getCapForSale()
        if self.grid.buy(self):
            self.st -= amount
    def buy(self):
        pass
    #TODO finish method where buy from microgrid and buy from maingrid

    def step(self):
        pass
    #TODO make players know forcast for next hour 
    #TODO current decision on the current hour
