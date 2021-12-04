from microgrid.microgrid import Microgrid
import matplotlib.pyplot as plt

def start():
    m = Microgrid(50)
    for i in range(100):
        m.step()
    print("Money for players")
"""     cash = []
    for i in m.players:
        cash.append(i.money)
        print("Player {} has:".format(i.id) + " " + str(i.money))
    plt.figure()
    plt.hist(cash,bins=len(cash))
    plt.show() """

if __name__ == "__main__":
    start()
