from microgrid.microgrid import Microgrid
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