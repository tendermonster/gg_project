from microgrid.microgrid import Microgrid
from microgrid.strategy import Strategy
import views
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def start():
    n_players = 10
    days = 1000
    randomize = True  # p and c don't change each step
    strategy = None
    # using random strategies for players
    """
    m = Microgrid(n_players, strategy=strategy, randomize=randomize)
    for i in range(days):
        m.step()
    main_sold = np.sum([i.sold_main for i in m.players])
    main_bought = np.sum([i.bought_main for i in m.players])
    micro_sold = np.sum([i.sold_micro for i in m.players])
    micro_bought = np.sum([i.bought_micro for i in m.players])
    print("random strategies for players")
    print("main sold ", main_sold)
    print("main bought ", main_bought)
    print("micro sold ", micro_sold)
    print("micro bought ", micro_bought)
    print("------------------------------------")

    print("Money for players")
    cash1 = [i.money for i in m.players]
    plt.figure()
    plt.title("random strategies for players")
    plt.hist(cash1, bins=len(cash1))
    # ----------------------------
    # using strategy GT
    s = Strategy(choice=Strategy.Choice.GT)
    m = Microgrid(n_players, s, randomize=randomize)
    for i in range(days):
        m.step()
    main_sold = np.sum([i.sold_main for i in m.players])
    main_bought = np.sum([i.bought_main for i in m.players])
    micro_sold = np.sum([i.sold_micro for i in m.players])
    micro_bought = np.sum([i.bought_micro for i in m.players])
    print("gt strategies for players")
    print("main sold ", main_sold)
    print("main bought ", main_bought)
    print("micro sold ", micro_sold)
    print("micro bought ", micro_bought)
    print("------------------------------------")
    print("Money for players")
    cash2 = [i.money for i in m.players]
    plt.figure()
    plt.title("strategy GT")
    plt.hist(cash2, bins=len(cash2))
    # ----------------------------
    """

    # using strategy always buy
    s = Strategy(choice=Strategy.Choice.ALWAYS_BUY)
    m = Microgrid(n_players, s, randomize=randomize)
    for i in range(days):
        m.step()
    main_sold = np.sum([i.sold_main for i in m.players])
    main_bought = np.sum([i.bought_main for i in m.players])
    micro_sold = np.sum([i.sold_micro for i in m.players])
    micro_bought = np.sum([i.bought_micro for i in m.players])
    print("buy strategies for players")
    print("main sold ", main_sold)
    print("main bought ", main_bought)
    print("micro sold ", micro_sold)
    print("micro bought ", micro_bought)
    print("------------------------------------")
    print("Money for players")
    cash3 = [i.money for i in m.players]
    plt.figure()
    plt.title("strategy always buy")
    plt.hist(cash3, bins=len(cash3))
    """
    # ----------------------------
    # using strategy always sell
    s = Strategy(choice=Strategy.Choice.ALWAYS_SELL)
    m = Microgrid(n_players, s, randomize=randomize)
    for i in range(days):
        m.step()
    main_sold = np.sum([i.sold_main for i in m.players])
    main_bought = np.sum([i.bought_main for i in m.players])
    micro_sold = np.sum([i.sold_micro for i in m.players])
    micro_bought = np.sum([i.bought_micro for i in m.players])
    print("sell strategies for players")
    print("main sold ", main_sold)
    print("main bought ", main_bought)
    print("micro sold ", micro_sold)
    print("micro bought ", micro_bought)
    print("------------------------------------")
    print("Money for players")
    cash4 = [i.money for i in m.players]
    plt.figure()
    plt.title("strategy always sell")
    plt.hist(cash4, bins=len(cash4))
    # ----------------------------
    # how did they perform
    print("Performance mean savings")
    print("Strategy random: {mean} ".format(mean=np.mean(cash1)))
    print("Strategy gt: {mean} ".format(mean=np.mean(cash2)))
    print("Strategy buy: {mean} ".format(mean=np.mean(cash3)))
    print("Strategy sell: {mean} ".format(mean=np.mean(cash4)))
    plt.show()
    """


if __name__ == "__main__":
    start()
