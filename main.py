from stringprep import c22_specials
from microgrid.microgrid import Microgrid
from microgrid.strategy import Strategy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import seaborn as sns

sns.set_theme()

def parameters():
    shift_b = 0
    params = set()
    for i in range(0,11):    
        a = list(np.around(np.abs(np.arange(1,0,-0.1)),decimals=2))
        b = list(np.around(np.abs(np.arange(0.1,1.1,0.1)),decimals=2))
        for j in range(0,i):
            a = a[-1:]+a[:-1]
        for j in range(0,shift_b):
            b = b[-1:]+b[:-1]
        params.update(tuple(zip(a,b)))
    params = sorted(list(params))
    return params

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
    #start()
    #parameter_search()
    n_players = 5
    days = 5
    randomize = True
    strategy = {
        "random": None,
        "gt": Strategy(choice=Strategy.Choice.GT),
        "sell": Strategy(choice=Strategy.Choice.ALWAYS_SELL),
        "buy": Strategy(choice=Strategy.Choice.ALWAYS_BUY),
    }
    m = Microgrid(n_players, strategy=strategy["gt"], randomize=randomize)
    params = parameters()

    start = time.time()
    cs = []
    cashs_gt = []
    cashs_sell = []
    cashs_buy = []
    count = 0
    for i in range(0,len(params)):
        if count == 20:
            break
        for j in params:
            BUY_MAIN = 1
            BUY_MICRO = params[i][1]
            SELL_MAIN = j[0]
            SELL_MICRO = j[1]

            if SELL_MICRO <= BUY_MICRO and SELL_MAIN <= BUY_MICRO:
                c = [BUY_MAIN,BUY_MICRO,SELL_MAIN,SELL_MICRO]
                cs.append(c)
                m = Microgrid(n_players, strategy=strategy["gt"], c = c, randomize=randomize)
                for g in range(days):
                    m.step()
                cash = np.mean([i.money for i in m.players])
                cashs_gt.append(cash)
                m = Microgrid(n_players, strategy=strategy["sell"], c = c, randomize=randomize)
                for g in range(days):
                    m.step()
                cash = np.mean([i.money for i in m.players])
                cashs_sell.append(cash)

                m = Microgrid(n_players, strategy=strategy["buy"], c = c, randomize=randomize)
                for g in range(days):
                    m.step()
                cash = np.mean([i.money for i in m.players])
                cashs_buy.append(cash)
        count += 1
    end = time.time()
    #print(cashs)
    #print(cs)
    #cashs_gt = sorted(cashs_gt)
    #cashs_sell = sorted(cashs_sell)
    print("mean money GT",np.mean(cashs_gt))
    print("mean money SELL",np.mean(cashs_sell))
    print("mean money BUY",np.mean(cashs_buy))
    plt.figure()
    #plt.title("diff params with GT")
    plt.plot(cashs_gt, label = "gt")
    #plt.title("diff params with SELL")
    plt.plot(cashs_sell, label = "sell")
    #plt.title("diff params with BUY")
    plt.plot(cashs_buy, label = "buy")
    plt.legend()

    df_cashs = pd.DataFrame(np.array([cashs_sell, cashs_gt, cashs_buy, cs]).T).sort_values(0).reset_index(drop = True)
    print(df_cashs.head())
    print(df_cashs.iloc[:,0:3])
    plt.title("ordered by selling for each simulation with different parameters")
    plt.figure()
    plt.plot(df_cashs.iloc[:,0:3], label=('sell','gt', 'buy'))
    plt.xlabel("Simulation")
    plt.ylabel("Money left")
    plt.legend()

    plt.figure()
    plt.title("parameters sets and values - offset by 1 (true range 0-1)")
    df_params = pd.DataFrame(df_cashs.iloc[:,3].tolist())
    df_params.iloc[:,1] = df_params.iloc[:,1] + 1
    df_params.iloc[:,2] = df_params.iloc[:,2] + 2
    df_params.iloc[:,3] = df_params.iloc[:,3] + 3
    plt.plot(df_params.iloc[:,1:4], 'o:', label=('BUY_MICRO','SELL_MAIN','SELL_MICRO'))
    plt.legend()
    plt.xlabel("Parameter set")
    plt.ylabel("Value - offset 1 for each")

    plt.figure()
    plt.title("parameters sets gt is better than sell")
    df_gt_sell = df_cashs[df_cashs.iloc[:,0] < df_cashs.iloc[:,1]]
    df_params_gt_sell = pd.DataFrame(df_gt_sell.iloc[:,3].tolist())
    df_params_gt_sell.iloc[:,1] = df_params_gt_sell.iloc[:,1] + 1
    df_params_gt_sell.iloc[:,2] = df_params_gt_sell.iloc[:,2] + 2
    df_params_gt_sell.iloc[:,3] = df_params_gt_sell.iloc[:,3] + 3
    plt.plot(df_params_gt_sell.iloc[:,1:4], 'o:', label=('BUY_MICRO','SELL_MAIN','SELL_MICRO'))
    plt.legend()
    plt.xlabel("Parameter set")
    plt.ylabel("Value - offset 1 for each")

    plt.figure()
    plt.title("selling main/micro price relation gt > sell")
    df_params_gt_sell.iloc[:,1] = df_params_gt_sell.iloc[:,1] - 1
    df_params_gt_sell.iloc[:,2] = df_params_gt_sell.iloc[:,2] - 2
    df_params_gt_sell.iloc[:,3] = df_params_gt_sell.iloc[:,3] - 3
    df_params_gt_sell['sell_main_micro_rel'] = df_params_gt_sell.iloc[:,2]/df_params_gt_sell.iloc[:,3]
    plt.plot(df_params_gt_sell['sell_main_micro_rel'])

    plt.figure()
    plt.title("parameters sets sell is better than gt")
    df_sell_gt = df_cashs[df_cashs.iloc[:,0] > df_cashs.iloc[:,1]]
    df_params_sell_gt = pd.DataFrame(df_sell_gt.iloc[:,3].tolist())
    df_params_sell_gt.iloc[:,1] = df_params_sell_gt.iloc[:,1] + 1
    df_params_sell_gt.iloc[:,2] = df_params_sell_gt.iloc[:,2] + 2
    df_params_sell_gt.iloc[:,3] = df_params_sell_gt.iloc[:,3] + 3
    plt.plot(df_params_sell_gt.iloc[:,1:4], 'o:', label=('BUY_MICRO','SELL_MAIN','SELL_MICRO'))
    plt.legend()
    plt.xlabel("Parameter set")
    plt.ylabel("Value - offset 1 for each")

    plt.figure()
    plt.title("selling main/micro price relation sell > gt")
    df_params_sell_gt.iloc[:,1] = df_params_sell_gt.iloc[:,1] - 1
    df_params_sell_gt.iloc[:,2] = df_params_sell_gt.iloc[:,2] - 2
    df_params_sell_gt.iloc[:,3] = df_params_sell_gt.iloc[:,3] - 3
    df_params_sell_gt['sell_main_micro_rel'] = df_params_sell_gt.iloc[:,2]/df_params_sell_gt.iloc[:,3]
    plt.plot(df_params_sell_gt['sell_main_micro_rel'])

    plt.figure()
    plt.title("parameters sets gt is better than sell")
    df_gt_sell = df_cashs[df_cashs.iloc[:,0] == df_cashs.iloc[:,1]]
    df_params_gt_sell = pd.DataFrame(df_gt_sell.iloc[:,3].tolist())
    df_params_gt_sell.iloc[:,1] = df_params_gt_sell.iloc[:,1] + 1
    df_params_gt_sell.iloc[:,2] = df_params_gt_sell.iloc[:,2] + 2
    df_params_gt_sell.iloc[:,3] = df_params_gt_sell.iloc[:,3] + 3
    plt.plot(df_params_gt_sell.iloc[:,1:4], 'o:', label=('BUY_MICRO','SELL_MAIN','SELL_MICRO'))
    plt.legend()
    plt.xlabel("Parameter set")
    plt.ylabel("Value - offset 1 for each")

    plt.figure()
    plt.title("selling main/micro price relation gt == sell")
    df_params_gt_sell.iloc[:,1] = df_params_gt_sell.iloc[:,1] - 1
    df_params_gt_sell.iloc[:,2] = df_params_gt_sell.iloc[:,2] - 2
    df_params_gt_sell.iloc[:,3] = df_params_gt_sell.iloc[:,3] - 3
    df_params_gt_sell['sell_main_micro_rel'] = df_params_gt_sell.iloc[:,2]/df_params_gt_sell.iloc[:,3]
    plt.plot(df_params_gt_sell['sell_main_micro_rel'])

    plt.figure()
    plt.title("difference of gt and sell and selling main/selling micro relation")
    df_diff_gt_sell = df_cashs.copy()
    df_diff_gt_sell= pd.concat([df_diff_gt_sell.iloc[:,0:3], pd.DataFrame(df_diff_gt_sell.iloc[:,3].tolist())], axis = 1).reset_index(drop = True)
    print(df_diff_gt_sell)
    df_diff_gt_sell['difference'] = df_diff_gt_sell.iloc[:,0] - df_diff_gt_sell.iloc[:,1]
    df_diff_gt_sell['sell_main_micro_rel'] = df_diff_gt_sell.iloc[:,5]/df_diff_gt_sell.iloc[:,6]
    plt.scatter(df_diff_gt_sell['difference'], df_diff_gt_sell['sell_main_micro_rel'])
    plt.xlabel("Difference of sell and gt")
    plt.ylabel("relation selling main/micro price")

    plt.figure()
    plt.title("difference/intersection GT and SELL")
    diff = set(cashs_gt)
    diff = diff.difference(set(cashs_sell))
    plt.plot(sorted(list(diff)),label="diff GT and SELL")
    intersection = set(cashs_gt)
    intersection = intersection.intersection(set(cashs_sell))
    plt.plot(sorted(list(intersection)),label="intersection GT and SELL")
    plt.legend()

    plt.figure()
    plt.title("difference/intersection GT and BUY")
    diff = set(cashs_gt)
    diff = diff.difference(set(cashs_buy))
    plt.plot(sorted(list(diff)),label="diff GT and BUY")
    intersection = set(cashs_gt)
    intersection = intersection.intersection(set(cashs_buy))
    plt.plot(sorted(list(intersection)),label="intersection GT and BUY")
    plt.legend()

    plt.figure()
    plt.title("difference/intersection SELL and BUY")
    diff = set(cashs_sell)
    diff = diff.difference(set(cashs_buy))
    plt.plot(sorted(list(diff)),label="diff SELL and BUY")
    intersection = set(cashs_sell)
    intersection = intersection.intersection(set(cashs_buy))
    plt.plot(sorted(list(intersection)),label="intersection SELL and BUY")
    plt.legend()

    # plot params
    c1 = []
    c2 = []
    for i in params:
        c1.append(i[0])
        c2.append(i[1])
    
    plt.figure()
    plt.title("tuple constant arrangement")
    plt.plot(c1,label="c1 fixed buy/sell")
    plt.plot(c2,label="c2 not fixed buy/sell")
    plt.legend()
    
    print(end - start)
    plt.show()
