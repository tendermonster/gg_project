from microgrid import Microgrid
def start():
    m = Microgrid(10)
    for i in range(7):
        print(m.players)
        print(m.getStorageForSale())
        print(m.getTotalC())
        print(m.getTotalP())
        print(m.currentPrice())
        m.step()

if __name__ == "__main__":
    start()