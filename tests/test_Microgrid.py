import sys
import os

sys.path.append(os.path.abspath("."))
from microgrid.microgrid import Microgrid
import unittest
import numpy as np


class TestMicrogridClass(unittest.TestCase):
    def setUp(self):
        self.m = Microgrid(n=10)

    def test_total_storage_for_sale(self):
        p = self.m.players
        s_should = np.sum([i.getCapForSale() for i in p])
        s_is = self.m.getStorageForSale()
        self.assertTrue(s_should == s_is)

    def test_total_storage_for_buy(self):
        p = self.m.players
        s_should = np.sum([i.getCapToBuy() for i in p])
        s_is = self.m.getStorageToBuy()
        self.assertTrue(s_should == s_is)


if __name__ == "__main__":
    unittest.main()
