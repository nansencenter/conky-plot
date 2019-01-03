import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd

cpus = 8
temps = 5

ifile = '/home/antonk/conky.txt'

w1 = 1


cpu_names = ['cpu%02d' % n for n in range(cpus)]
freq_names = ['freq%02d' % n for n in range(cpus)]
temp_names = ['temp%02d' % n for n in range(temps)]
names = ['d0', 'd1']+cpu_names+freq_names+temp_names

df = pd.read_csv(ifile, sep=" ", header=None, parse_dates={'time': [0,1]}, names=names).set_index('time')

fig, axes = plt.subplots(nrows=3, ncols=1, sharex='col')

df.rolling(w1).mean()[::w1].plot(y=cpu_names, ax=axes[0])

df.rolling(w1).mean()[::w1].plot(y=freq_names, ax=axes[1])

df.rolling(w1).mean()[::w1].plot(y=temp_names, ax=axes[2])
plt.show()
