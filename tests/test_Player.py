import sys
import os
import numpy as np

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
        p2_buy_should = abs(20 - 20 + 70 - 80)
        p2_buy_is = self.p2.getCapToBuy()
        self.assertTrue(p2_buy_should == p2_buy_is)

    def testBuyStrategie(self):
        m = Microgrid(n=5, strategy=self.str)
        p0 = m.players[0]
        p0.step()

    def testBoughtSoldInsideMicro(self):
        m = Microgrid(n=10, strategy=self.str, randomize=False)
        for i in range(20):
            m.step()
        total_bought = np.sum([i.bought_micro for i in m.players])
        total_sold = np.sum([i.sold_micro for i in m.players])
        diff = abs(total_bought - total_sold)
        self.assertTrue(diff < 0.5)

    def testBoughtSoldInsideMicroEachStep(self):
        m = Microgrid(n=10, strategy=self.str, randomize=False)
        for i in range(20):
            m.step()
            total_bought = np.sum([i.bought_micro for i in m.players])
            total_sold = np.sum([i.sold_micro for i in m.players])
            diff = abs(total_bought - total_sold)
            self.assertTrue(diff < 0.5)

    def testBoughtSold(self):
        # simple scenario
        p1 = Player(
                None,
                1,
                Player.States.DO_NOTHING,
                strategy=Strategy(Strategy.Choice.ALWAYS_SELL),
                p=100,
                c=70,
                b=20,
                randomize=False,
            )

        p2 = Player(
                None,
                2,
                Player.States.DO_NOTHING,
                strategy=Strategy(Strategy.Choice.GT),
                p=60,
                c=100,
                b=20,
                randomize=False,
            )

        m = Microgrid(n = 2, strategy = None, randomize = False)
        m.players[0] = p1
        m.players[0].grid = m
        m.players[1] = p2
        m.players[1].grid = m

        m.players[0].step()
        m.players[1].step()

        p1_sold_micro_should = 30
        p1_sold_main_should = 0
        p2_bought_micro_should = 30
        p2_bought_main_should = 10

        self.assertTrue(m.players[0].sold_micro == p1_sold_micro_should)
        self.assertTrue(m.players[0].sold_main == p1_sold_main_should)
        self.assertTrue(m.players[1].bought_micro == p2_bought_micro_should)
        self.assertTrue(m.players[1].bought_main == p2_bought_main_should)

if __name__ == "__main__":
    unittest.main()
