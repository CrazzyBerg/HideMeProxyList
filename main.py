import time
from HideME import HideME

if __name__ == '__main__':
    start_time = time.time()
    proxy = HideME(url='/proxy-list/', max_time=500, types='s', count=70)
    print(proxy.get())
    print("\n--- %s seconds ---" % (time.time() - start_time))
