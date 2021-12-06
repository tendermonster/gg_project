from microgrid.microgrid import Microgrid
from microgrid.strategy import Strategy
import views
import matplotlib.pyplot as plt
import numpy as np


def start():
    n_players = 5
    days = 1000
    randomize = True  # p and c don't change each step
    # using random strategies for players
    m = Microgrid(n_players, None, randomize=randomize)
    print(views.initial_playermatrix(m))
    total_series = views.register_stepseries(m)  # initial
    for i in range(days):
        step_series = m.step()
        total_series = views.series_append(total_series, step_series)
    print(total_series["money"])
    print(total_series["b"])
    print(total_series["c"])
    print(total_series["p"])
    print("Money for players")
    cash1 = []
    for i in m.players:
        cash1.append(i.money)
        # print("Player {} has:".format(i.id) + " " + str(i.money))
    plt.figure()
    plt.title("random strategies for players")
    plt.hist(cash1, bins=len(cash1))
    # ----------------------------
    # using strategy GT
    s = Strategy(choice=Strategy.Choice.GT)
    m = Microgrid(n_players, s, randomize=randomize)
    for i in range(days):
        m.step()
    print("Money for players")
    cash2 = []
    for i in m.players:
        cash2.append(i.money)
        # print("Player {} has:".format(i.id) + " " + str(i.money))
    plt.figure()
    plt.title("strategy GT")
    plt.hist(cash2, bins=len(cash2))
    # ----------------------------

    # using strategy always buy
    s = Strategy(choice=Strategy.Choice.ALWAYS_BUY)
    m = Microgrid(n_players, s, randomize=randomize)
    for i in range(days):
        m.step()
    print("Money for players")
    cash3 = []
    for i in m.players:
        cash3.append(i.money)
        print("Player {} has:".format(i.id) + " " + str(i.money))
    plt.figure()
    plt.title("strategy always buy")
    plt.hist(cash3, bins=len(cash3))
    # ----------------------------
    # using strategy always sell
    s = Strategy(choice=Strategy.Choice.ALWAYS_SELL)
    m = Microgrid(n_players, s, randomize=randomize)
    for i in range(days):
        m.step()
    print("Money for players")
    cash4 = []
    for i in m.players:
        cash4.append(i.money)
        # print("Player {} has:".format(i.id) + " " + str(i.money))
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


if __name__ == "__main__":
    start()
