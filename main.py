from microgrid.microgrid import Microgrid
def start():
    m = Microgrid(10)
    for i in range(7):
        print("total storage for sale:" + str(m.getStorageForSale()))
        print("total consumption: "+str(m.getTotalC()))
        print("total production: "+str(m.getTotalP()))
        m.step()

if __name__ == "__main__":
    start()