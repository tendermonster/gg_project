from microgrid.microgrid import Microgrid
from microgrid.strategy import Strategy
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set_theme()

def start():
    # this values show pretty much perfect normal distribution
    # n_players = 500
    # days = 100
    n_players = 500
    days = 100
    randomize = True  # p and c don't change each step
    strategy = {
        "random": None,
        "gt": Strategy(choice=Strategy.Choice.GT),
        "sell": Strategy(choice=Strategy.Choice.ALWAYS_SELL),
        "buy": Strategy(choice=Strategy.Choice.ALWAYS_BUY),
    }
    counter = 0
    avg_battery_levels = []
    for k in strategy:
        # using random strategies for players
        m = Microgrid(n_players, strategy=strategy[k], randomize=randomize)
        for i in range(days):
            m.step()

        avg_batt_storage = None
        for i in m.players:
            if avg_batt_storage is None:
                avg_batt_storage = i.battery_storage
            avg_batt_storage = np.add(avg_batt_storage,i.battery_storage)
        avg_batt_storage = avg_batt_storage/len(m.players)
        avg_battery_levels.append(avg_batt_storage)

        type_where="main"
        mode = "sold"
        sold_main = [i.sold_main for i in m.players]
        main_sold = np.sum(sold_main)
        plt.figure()
        plt.title("Sold to maingrid with strategy {s}".format(s=k))
        plt.xlabel("Player")
        plt.ylabel("Energy units sold")
        plt.plot(sold_main)
        plt.savefig("figures/{m}_{w}_{s}_{c}.png".format(s=k,c=counter,w=type_where,m=mode))
        plt.close()
        
        mode = "bought"
        bought_main = [i.bought_main for i in m.players]
        main_bought = np.sum(bought_main)
        plt.figure()
        plt.title("Bought from maingrid with strategy {s}".format(s=k))
        plt.xlabel("Player")
        plt.ylabel("Energy units bought")
        plt.plot(bought_main)
        plt.savefig("figures/{m}_{w}_{s}_{c}.png".format(s=k,c=counter,w=type_where,m=mode))
        plt.close()


        type_where="micro"
        mode = "sold"
        sold_micro = [i.sold_micro for i in m.players]
        micro_sold = np.sum(sold_micro)
        plt.figure()
        plt.title("Sold to smartgrid with strategy {s}".format(s=k))
        plt.xlabel("Player")
        plt.ylabel("Energy units sold")
        plt.plot(sold_micro)
        plt.savefig("figures/{m}_{w}_{s}_{c}.png".format(s=k,c=counter,w=type_where,m=mode))
        plt.close()

        mode = "bought"
        bought_micro = [i.bought_micro for i in m.players]
        micro_bought = np.sum(bought_micro)
        plt.figure()
        plt.title("Bought from smartgrid with strategy {s}".format(s=k))
        plt.xlabel("Player")
        plt.ylabel("Energy units bought")
        plt.plot(bought_micro)
        plt.savefig("figures/{m}_{w}_{s}_{c}.png".format(s=k,c=counter,w=type_where,m=mode))
        plt.close()

        mode = "money"
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
        plt.xlabel("Money left")
        plt.ylabel("Occurrence")
        avg_cash = np.sum(cash)/len(cash)
        plt.axvline(avg_cash,c='r',linewidth=5.0,label="average")
        plt.hist(cash, bins=len(cash),color = "skyblue", ec="skyblue")
        plt.legend()
        plt.savefig("figures/{m}_{s}_{c}.png".format(s=k,c=counter,m=mode))
        plt.close()
        counter +=1
    #plt.show()
    plt.figure()
    plt.title("avg battery levels of the players")
    plt.xlabel("days of simulation")
    plt.ylabel("battery level")
    s = ["random","gt","sell(same as gt)","buy"]
    for i in range(len(avg_battery_levels)):
        plt.plot(avg_battery_levels[i],label=s[i])
    mode = "battery_level"
    plt.legend()
    plt.savefig("figures/{m}_{c}.png".format(c=counter,m=mode))
    plt.close()


if __name__ == "__main__":
    start()
