from microgrid.microgrid import Microgrid
from microgrid.strategy import Strategy
import matplotlib.pyplot as plt

def start():
    #using strategy GT
    s = Strategy(choice=Strategy.Choice.GT)
    m = Microgrid(50,s)
    for i in range(500):
        m.step()
    print("Money for players")
    cash = []
    for i in m.players:
        cash.append(i.money)
        print("Player {} has:".format(i.id) + " " + str(i.money))
    plt.figure()
    plt.title("strategy GT")
    plt.hist(cash,bins=len(cash))
    # ----------------------------
    #using strategy always buy
    s = Strategy(choice=Strategy.Choice.ALWAYS_BUY)
    m = Microgrid(50,s)
    for i in range(500):
        m.step()
    print("Money for players")
    cash = []
    for i in m.players:
        cash.append(i.money)
        print("Player {} has:".format(i.id) + " " + str(i.money))
    plt.figure()
    plt.title("strategy always buy")
    plt.hist(cash,bins=len(cash))
    # ----------------------------
    #using strategy always sell
    s = Strategy(choice=Strategy.Choice.ALWAYS_SELL)
    m = Microgrid(50,s)
    for i in range(500):
        m.step()
    print("Money for players")
    cash = []
    for i in m.players:
        cash.append(i.money)
        print("Player {} has:".format(i.id) + " " + str(i.money))
    plt.figure()
    plt.title("strategy always sell")
    plt.hist(cash,bins=len(cash))
    # ----------------------------
    plt.show()

if __name__ == "__main__":
    start()
