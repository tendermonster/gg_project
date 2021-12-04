import sys
import os

from microgrid.strategy import Strategy

sys.path.append(os.path.abspath("."))
from microgrid.player import Player
from microgrid.microgrid import Microgrid
import unittest


class TestPlayerClass(unittest.TestCase):
    def setUp(self):
        self.str = Strategy(Strategy.Choice.GT)
        self.p0 = Player(
            None,
            0,
            Player.States.DO_NOTHING,
            strategy=self.str,
            p=100,
            c=100,
            b=100,
            randomize=False,
        )
        self.p1 = Player(
            None,
            1,
            Player.States.DO_NOTHING,
            strategy=self.str,
            p=100,
            c=80,
            b=70,
            randomize=False,
        )

    def testEqualityOfPlayer(self):
        self.assertTrue(self.p0 == self.p0)
        self.assertTrue(self.p0 != self.p1)

    def testStorageAfterInitialization(self):
        p0_should = 80
        self.assertTrue(self.p0.getAvailableStorage() == p0_should)
        p1_should = 70
        self.assertTrue(self.p1.getAvailableStorage() == p1_should)

    def testBuySellAvailabilityAfterInitialization(self):
        p0_buy_should = 0
        p0_buy_is = self.p0.getCapToBuy()
        p0_sell_should = 80
        p0_sell_is = self.p0.getCapForSale()
        self.assertTrue(p0_buy_is == p0_buy_should)
        self.assertTrue(p0_sell_is == p0_sell_should)
        p1_buy_should = 0
        p1_sell_should = 70
        self.assertTrue(self.p1.getCapToBuy() == p1_buy_should)
        self.assertTrue(self.p1.getCapForSale() == p1_sell_should)
        # testing a nice buy scenario
        self.p2 = Player(
            None,
            2,
            Player.States.DO_NOTHING,
            strategy=self.str,
            p=70,
            c=80,
            b=20,
            randomize=False,
        )
        p2_buy_should = abs(20 - 20 + 70 - 80)
        p2_buy_is = self.p2.getCapToBuy()
        self.assertTrue(p2_buy_should == p2_buy_is)

    def testBuyStrategie(self):
        m = Microgrid(n=5, strategy=self.str)
        p0 = m.players[0]
        p0.step()


if __name__ == "__main__":
    unittest.main()
