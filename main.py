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
        a = list(np.around(np.abs(np.arange(1,-0.1,-0.1)),decimals=2))
        b = list(np.around(np.abs(np.arange(0,1.1,0.1)),decimals=2))
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
    n_players = 5
    days = 12
    randomize = True
    strategy = {
        "random": None,
        "gt": Strategy(choice=Strategy.Choice.GT),
        "sell": Strategy(choice=Strategy.Choice.ALWAYS_SELL),
        "buy": Strategy(choice=Strategy.Choice.ALWAYS_BUY),
    }
    params = parameters()
    unconstrained = 0
    start = time.time()
    cs = []
    cashs_gt = []
    cashs_sell = []
    cashs_buy = []
    count = 0
    for i in range(0,len(params)):
        # if count == 20:
        #      break
        for j in params:
            if unconstrained == 1:
                BUY_MAIN = params[i][0]
            else:
                BUY_MAIN = 1
            BUY_MICRO = params[i][1]
            SELL_MAIN = j[0]
            SELL_MICRO = j[1]

            if (SELL_MICRO <= BUY_MICRO and SELL_MAIN <= BUY_MICRO) or unconstrained == 1:
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
    plt.title("Money left after simulation for each parameter")
    plt.ylabel("Money left")
    plt.xlabel("Parameter with ID")
    plt.plot(cashs_gt, label = "gt")
    plt.plot(cashs_sell, label = "sell")
    plt.plot(cashs_buy, label = "buy")
    plt.legend(loc = 'best')

    df_cashs = pd.DataFrame(np.array([cashs_sell, cashs_gt, cashs_buy, cs]).T, columns=['sell','gt','buy','params']).sort_values('sell').reset_index(drop=True)
    df_cashs_unique = df_cashs.drop_duplicates(subset = ['sell','gt','buy'])
    """
    plt.figure()
    plt.title("constrained search space final money left")
    plt.plot(df_cashs_unique.iloc[:,2], label='buy')
    plt.plot(df_cashs_unique.iloc[:,1], label='gt')
    plt.plot(df_cashs_unique.iloc[:,0], label='sell')
    plt.xlabel("Simulation ID")
    plt.ylabel("Money left")
    plt.legend(loc = 'lower right')
    plt.savefig("figures/constrained_money_left.png", bbox_inches = "tight")

    plt.figure()

    plt.title("constrained parameters values")
    df_params = pd.DataFrame(df_cashs.iloc[:,3].tolist()).reset_index(drop=True).reset_index()
    df_params.iloc[:,2] = df_params.iloc[:,2] + 1
    df_params.iloc[:,3] = df_params.iloc[:,3] + 2
    df_params.iloc[:,4] = df_params.iloc[:,4] + 3

    #colors 
    labels = ['% Buy from main','% Buy from micro','% Sell to main','% Sell to micro']
    x = df_params['index']
    ys1 = df_params.iloc[:,1]
    ys2 = df_params.iloc[:,2]
    ys3 = df_params.iloc[:,3]
    ys4 = df_params.iloc[:,4]

    plt.scatter(x, ys1, label=labels[0], marker = '.')
    plt.scatter(x, ys2, label=labels[1], marker = '.')
    plt.scatter(x, ys3, label=labels[2], marker = '.')
    plt.scatter(x, ys4, label=labels[3], marker = '.')
    #plt.plot(df_params.iloc[:,0:4], 'o:', label=('BUY_MAIN','BUY_MICRO','SELL_MAIN','SELL_MICRO'))
    plt.legend(bbox_to_anchor=(1.04,0))
    plt.xlabel("Simulation ID")
    plt.ylabel("Values")
    plt.savefig("figures/constrained_parameters_sets.png", bbox_inches = "tight")
    df_params.drop(columns ='index', axis = 1, inplace = True)

    plt.figure()
    plt.title("constrained parameters - gt is better than sell")
    df_gt_sell = df_cashs[df_cashs.iloc[:,0] < df_cashs.iloc[:,1]]
    df_params_gt_sell = pd.DataFrame(df_gt_sell.iloc[:,3].tolist())
    df_params_gt_sell.iloc[:,1] = df_params_gt_sell.iloc[:,1] + 1
    df_params_gt_sell.iloc[:,2] = df_params_gt_sell.iloc[:,2] + 2
    df_params_gt_sell.iloc[:,3] = df_params_gt_sell.iloc[:,3] + 3
    df_params_gt_sell = df_params_gt_sell.reset_index(drop =True).reset_index()
    plt.scatter(df_params_gt_sell['index'], df_params_gt_sell.iloc[:,1], label='% Buy from main', marker = '.')
    plt.scatter(df_params_gt_sell['index'], df_params_gt_sell.iloc[:,2], label='% Buy from micro', marker = '.')
    plt.scatter(df_params_gt_sell['index'], df_params_gt_sell.iloc[:,3], label='% Sell to main', marker = '.')
    plt.scatter(df_params_gt_sell['index'], df_params_gt_sell.iloc[:,4], label='% Sell to micro', marker = '.')
    #plt.plot(df_params_gt_sell.iloc[:,0:4], 'o:', label=('BUY_MAIN','BUY_MICRO','SELL_MAIN','SELL_MICRO'))
    plt.legend(bbox_to_anchor=(1.04,0))
    plt.xlabel("Simulation ID")
    plt.ylabel("Values")
    plt.savefig("figures/constrained_parameters_sets_gtbettersell.png", bbox_inches = "tight")

    # plt.figure()
    # plt.title("Price ratio - gt is better than sell")
    # df_params_gt_sell.iloc[:,1] = df_params_gt_sell.iloc[:,1] - 1
    # df_params_gt_sell.iloc[:,2] = df_params_gt_sell.iloc[:,2] - 2
    # df_params_gt_sell.iloc[:,3] = df_params_gt_sell.iloc[:,3] - 3
    # df_params_gt_sell['sell_main_micro_rel'] = df_params_gt_sell.iloc[:,2]/df_params_gt_sell.iloc[:,3]
    # plt.plot(df_params_gt_sell['sell_main_micro_rel'])
    # plt.legend()
    # plt.xlabel("Simulation ID")
    # plt.ylabel("Values")

    plt.figure()
    plt.title("constrained parameters - sell is better than gt")
    df_sell_gt = df_cashs[df_cashs.iloc[:,0] > df_cashs.iloc[:,1]]
    df_params_sell_gt = pd.DataFrame(df_sell_gt.iloc[:,3].tolist())
    df_params_sell_gt.iloc[:,1] = df_params_sell_gt.iloc[:,1] + 1
    df_params_sell_gt.iloc[:,2] = df_params_sell_gt.iloc[:,2] + 2
    df_params_sell_gt.iloc[:,3] = df_params_sell_gt.iloc[:,3] + 3
    df_params_sell_gt = df_params_sell_gt.reset_index(drop=True).reset_index()
    plt.scatter(df_params_sell_gt['index'], df_params_sell_gt.iloc[:,1], label='% Buy from main', marker = '.')
    plt.scatter(df_params_sell_gt['index'], df_params_sell_gt.iloc[:,2], label='% Buy from micro', marker = '.')
    plt.scatter(df_params_sell_gt['index'], df_params_sell_gt.iloc[:,3], label='% Sell to main', marker = '.')
    plt.scatter(df_params_sell_gt['index'], df_params_sell_gt.iloc[:,4], label='% Sell to micro', marker = '.')
    #plt.plot(df_params_sell_gt.iloc[:,0:4], 'o:', label=('BUY_MAIN','BUY_MICRO','SELL_MAIN','SELL_MICRO'))
    plt.legend(bbox_to_anchor=(1.04,0))
    plt.xlabel("Simulation ID")
    plt.ylabel("Values")
    plt.savefig("figures/constrained_parameters_sets_sellbettergt.png", bbox_inches = "tight")


    # plt.figure()
    # plt.title("selling main/micro price relation sell > gt")
    # df_params_sell_gt.iloc[:,1] = df_params_sell_gt.iloc[:,1] - 1
    # df_params_sell_gt.iloc[:,2] = df_params_sell_gt.iloc[:,2] - 2
    # df_params_sell_gt.iloc[:,3] = df_params_sell_gt.iloc[:,3] - 3
    # df_params_sell_gt['sell_main_micro_rel'] = df_params_sell_gt.iloc[:,2]/df_params_sell_gt.iloc[:,3]
    # plt.plot(df_params_sell_gt['sell_main_micro_rel'])

    plt.figure()
    plt.title("constrained parameters - gt equal to sell")
    df_gt_sell = df_cashs[df_cashs.iloc[:,0] == df_cashs.iloc[:,1]]
    df_params_gt_sell = pd.DataFrame(df_gt_sell.iloc[:,3].tolist())
    df_params_gt_sell.iloc[:,1] = df_params_gt_sell.iloc[:,1] + 1
    df_params_gt_sell.iloc[:,2] = df_params_gt_sell.iloc[:,2] + 2
    df_params_gt_sell.iloc[:,3] = df_params_gt_sell.iloc[:,3] + 3
    df_params_gt_sell = df_params_gt_sell.reset_index(drop=True).reset_index()
    plt.scatter(df_params_gt_sell['index'], df_params_gt_sell.iloc[:,1], label='% Buy from main', marker = '.')
    plt.scatter(df_params_gt_sell['index'], df_params_gt_sell.iloc[:,2], label='% Buy from micro', marker = '.')
    plt.scatter(df_params_gt_sell['index'], df_params_gt_sell.iloc[:,3], label='% Sell to main', marker = '.')
    plt.scatter(df_params_gt_sell['index'], df_params_gt_sell.iloc[:,4], label='% Sell to micro', marker = '.')
    #plt.plot(df_params_gt_sell.iloc[:,0:4], 'o:', label=('BUY_MAIN','BUY_MICRO','SELL_MAIN','SELL_MICRO'))
    plt.legend(bbox_to_anchor=(1.04,0))
    plt.xlabel("Simulation ID")
    plt.ylabel("Values")
    plt.savefig("figures/constrained_parameters_sets_sellequalgt.png", bbox_inches = "tight")

    # plt.figure()
    # plt.title("selling main/micro price relation gt == sell")
    # df_params_gt_sell.iloc[:,1] = df_params_gt_sell.iloc[:,1] - 1
    # df_params_gt_sell.iloc[:,2] = df_params_gt_sell.iloc[:,2] - 2
    # df_params_gt_sell.iloc[:,3] = df_params_gt_sell.iloc[:,3] - 3
    # df_params_gt_sell['sell_main_micro_rel'] = df_params_gt_sell.iloc[:,2]/df_params_gt_sell.iloc[:,3]
    # plt.plot(df_params_gt_sell['sell_main_micro_rel'])
    """

    plt.figure()
    plt.title("difference of gt and sell and selling main/selling micro relation")
    df_diff_gt_sell = df_cashs.copy()
    df_diff_gt_sell= pd.concat([df_diff_gt_sell.iloc[:,0:3], pd.DataFrame(df_diff_gt_sell.iloc[:,3].tolist())], axis = 1).reset_index(drop = True)
    df_diff_gt_sell['difference'] = df_diff_gt_sell.iloc[:,0] - df_diff_gt_sell.iloc[:,1]
    df_diff_gt_sell['difference'].replace([np.inf, -np.inf], np.nan, inplace=True)
    x_diff = df_diff_gt_sell['difference'].to_numpy()
    x_diff[x_diff == 0] = np.nan
    df_diff_gt_sell['sell_main_micro_rel'] = df_diff_gt_sell.iloc[:,5]/df_diff_gt_sell.iloc[:,6]
    df_diff_gt_sell['sell_main_micro_rel'].replace([np.inf, -np.inf], np.nan, inplace=True)
    y_ratio = df_diff_gt_sell['sell_main_micro_rel'].to_numpy()
    plt.axvspan(min(x_diff), 0, facecolor='b', alpha=0.5,label = "more profitable for gt strategy")
    plt.axvspan(0,max(x_diff)*1.1, facecolor='g', alpha=0.5,label = "more profitable for sell strategy")
    plt.scatter(x_diff, y_ratio, marker = '.',color = "black")
    plt.xlabel("Difference of money left for always sell and gt")
    plt.ylabel("Ratio between selling main/selling micro prices")
    plt.legend()
    plt.savefig("figures/constrained_ratio_diff.png")
    plt.show()

    """
    plt.figure()
    plt.title("difference of gt and sell and selling main/selling micro relation")
    df_diff_gt_sell = df_cashs.copy()
    df_diff_gt_sell= pd.concat([df_diff_gt_sell.iloc[:,0:3], pd.DataFrame(df_diff_gt_sell.iloc[:,3].tolist())], axis = 1).reset_index(drop = True)
    df_diff_gt_sell['difference'] = df_diff_gt_sell.iloc[:,0] - df_diff_gt_sell.iloc[:,1]
    x_diff = np.nan_to_num(df_diff_gt_sell['difference'].to_numpy())
    df_diff_gt_sell['sell_main_micro_rel'] = df_diff_gt_sell.iloc[:,5]/df_diff_gt_sell.iloc[:,6]
    y_ratio = np.nan_to_num(df_diff_gt_sell['sell_main_micro_rel'].to_numpy())
    plt.scatter(x_diff, y_ratio, marker = '.')
    plt.xlabel("Difference of money left for always sell and gt")
    plt.ylabel("Ratio between selling main/selling micro prices")
    plt.savefig("figures/constrained_ratio_diff.png")
    plt.show()
    """

    """

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
    """
