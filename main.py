from microgrid.microgrid import Microgrid


def start():
    m = Microgrid(50)
    for i in range(60):
        # print("total storage for sale:" + str(m.getStorageForSale()))
        # print(f"total energy buying: {m.getStorageToBuy()}")
        m.step()
    print("Money for players")
    for i in m.players:
        print("Player {} has:".format(i.id) + " " + str(i.money))


if __name__ == "__main__":
    start()
