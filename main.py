from microgrid.microgrid import Microgrid

def start():
    m = Microgrid(5)
    for i in range(6):
        print("total storage for sale:" + str(m.getStorageForSale()))
        print(f"total energy buying: {m.getStorageToBuy()}")
        m.step()

if __name__ == "__main__":
    start()
    #m = Microgrid(5)
    #print(gt.comb_strategies(m))
    #todo name the values 
    #print(gt.utility_function(m,(1, -1, 1, -1, 1)))
    #print(gt.strategies_utilities(m))