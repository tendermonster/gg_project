from microgrid.microgrid import Microgrid
from microgrid.strategy import Strategy
import matplotlib.pyplot as plt
import numpy as np


def start():
    #this values show pretty much perfect normal distribution
    #n_players = 500
    #days = 100
    n_players = 200
    days = 100
    randomize = True  # p and c don't change each step
    strategy = {"random": None,
                "gt": Strategy(choice=Strategy.Choice.GT),
                "sell": Strategy(choice=Strategy.Choice.ALWAYS_SELL),
                "buy": Strategy(choice=Strategy.Choice.ALWAYS_BUY)}
    for k in strategy:
        # using random strategies for players
        m = Microgrid(n_players, strategy=strategy[k], randomize=randomize)
        for i in range(days):
            m.step()
        main_sold = np.sum([i.sold_main for i in m.players])
        main_bought = np.sum([i.bought_main for i in m.players])
        micro_sold = np.sum([i.sold_micro for i in m.players])
        micro_bought = np.sum([i.bought_micro for i in m.players])
        print("{s} strategy for players".format(s=k))
        print("main sold ", main_sold)
        print("main bought ", main_bought)
        print("micro sold ", micro_sold)
        print("micro bought ", micro_bought)
        print("simulated {days} days".format(days=m.day))
        cash = [i.money for i in m.players]
        print("average money for players: {money}".format(money=np.mean(cash)))
        print("------------------------------------")
        plt.figure()
        plt.title("{s} strategy for players".format(s=k))
        plt.hist(cash, bins=len(cash))
    plt.show()


if __name__ == "__main__":
    start()
