from microgrid.microgrid import Microgrid
import gt

def start():
    m = Microgrid(5)
    for i in range(1):
        print("total storage for sale:" + str(m.getStorageForSale()))
        print(f"total energy buying: {m.getStorageToBuy()}")
        print("total consumption: "+str(m.getTotalC()))
        print("total production: "+str(m.getTotalP()))
        m.step()

if __name__ == "__main__":
    start()

m = Microgrid(5)
gt.comb_strategies(m)
gt.utility_function(m,(1, -1, 1, -1, 1))
gt.strategies_utilities(m)