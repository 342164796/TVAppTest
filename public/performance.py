# -*- coding:utf-8 -*-
import sys
sys.path.append('..')
import lib.Logging as L
def data_marker(cpu, mem, h_cpu, h_mem, path):
    import matplotlib
    matplotlib.use('Agg')
    import pylab as pl
    pl.plot(cpu, 'r')
    pl.plot(mem, 'g')
    pl.title('performance')
    pl.xlabel('second')
    pl.ylabel('percent')
    pl.plot(cpu, color="red", linewidth=2.5, linestyle="-",label="this_cpu")
    pl.plot(mem, color="blue", linewidth=2.5, linestyle="-",label="this_mem")
    if h_mem is not None:
        pl.plot(h_cpu, color="magenta", linewidth=2.5,linestyle="-",label="history_cpu")
        pl.plot(h_mem, color="green",linewidth=2.5,linestyle="-",label="history_mem")
    pl.legend(loc='upper left')
    pl.xlim(0.0,len(mem))
    pl.ylim(0.0, 100.0)
    pl.savefig(path)
    L.Logging.debug('Report: %s' % path)
  #  pl.show()
    pl.close()
if __name__ == "__main__":
    import random
    def get_num():
        lst=[]
        for i in range(10):
            lst.append(random.randint(1,60))
        return lst
    for i in range(1):
        data_marker(get_num(),get_num(),get_num(),get_num(),'%s.png' % i)
