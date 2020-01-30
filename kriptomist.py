"""
== Kriptomist ==

Analyze flow in the world of crypto.
"""

import logging
log = logging.getLogger('kriptomist')

import sys
from pprint import pprint

from coin import Coin
from coinmarketcap import Coinmarketcap
from redditmetrics import Redditmetrics
from util import div0, dump_html
import draw

class Kriptomist:
    def __init__(self, coin):
        self.coin = coin
        self.compute_stats()
        
    def compute_stats(self):
        p = [a[1] for a in self.coin.btc]
        if self.coin.name == 'bitcoin':
            p = [a[1] for a in self.coin.usd]
        subs = [a[1] for a in self.coin.subs]
        flw = [a[1] for a in self.coin.flw]
        
        # cmc
        self.price28 = p[-1] - p[-29]
        self.price28_rel = div0(p[-1], p[-29])
        
        # reddit
        self.subs28 = subs[-1] - subs[-29]
        self.subs7 = subs[-1] - subs[-8]
        self.subs1 = subs[-1] - subs[-2]

        self.subs28_rel = div0(subs[-1], subs[-29])
        self.subs7_rel = div0(subs[-1], subs[-8])
        self.subs1_rel = div0(subs[-1], subs[-2])
        
        self.subs7_acc = div0( (self.subs7_rel * 4 - 3), self.subs28_rel )
        self.subs1_acc = div0( (self.subs1_rel * 7 - 6), self.subs7_rel )
        
        # reddit compare
        self.cmp28 = div0(self.subs28_rel**2, self.price28_rel)
        self.cmp7 = div0(self.subs7_rel**2, (3 + self.price28_rel) / 4)
        self.cmp1 = div0(self.subs1_rel**2, (27 + self.price28_rel) / 28)

        # reddit score
        self.score = self.cmp28 * (self.subs1_acc ** 4) * (self.subs7_acc ** 2)

        # twitter
        self.flw28 = flw[-1] - flw[-29]
        self.flw7 = flw[-1] - flw[-8]
        self.flw1 = flw[-1] - flw[-2]

        self.flw28_rel = div0(flw[-1], flw[-29])
        self.flw7_rel = div0(flw[-1], flw[-8])
        self.flw1_rel = div0(flw[-1], flw[-2])
        
        self.flw7_acc = div0( (self.flw7_rel * 4 - 3), self.flw28_rel )
        self.flw1_acc = div0( (self.flw1_rel * 7 - 6), self.flw7_rel )
        
        # twitter compare
        self.tcmp28 = div0(self.flw28_rel**2, self.price28_rel)
        self.tcmp7 = div0(self.flw7_rel**2, (3 + self.price28_rel) / 4)
        self.tcmp1 = div0(self.flw1_rel**2, (27 + self.price28_rel) / 28)

        # twitter score
        self.tscore = self.tcmp28 * (self.flw1_acc ** 4) * (self.flw7_acc ** 2)


    def display(self):
        print("[#{}: {}]".format(self.coin.cmc.rank, self.coin.name))
        pprint(self.__dict__)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    if sys.argv[1:]:
        name = sys.argv[1]
        coin = Coin(name)
        km = Kriptomist(coin)
        km.display()
        draw.draw_coin(coin)
    else:
        KMS = []
        coins = Coinmarketcap.list_coins()
        for i, data in enumerate(coins):
            try:
                coin = Coin(data["slug"], data=data)
                km = Kriptomist(coin)
                km.display()
                KMS.append(km)
            except:
                log.exception("Skipping {}".format(data["slug"]))
        dump_html(KMS)
        
    