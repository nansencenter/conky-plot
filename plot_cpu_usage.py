#!/usr/bin/env python
import sys
import argparse
import datetime as dt

import matplotlib.pyplot as plt
import pandas as pd

parser = argparse.ArgumentParser(description="Plot CPU usage, frequency and temperature")
parser.add_argument('-n', '--hours', type=int, default=2, help='Show plots for the last <n> hours')
parser.add_argument('-w', '--window', type=int, default=3, help='Sliding average over <w> minutes')
parser.add_argument('-s', '--step', type=int, default=1, help='Plot each <s> record')
args = parser.parse_args(sys.argv[1:])

cpus = 8
temps = 5

plot_style = dict(legend = False)

ifile = '/home/antonk/conky.txt'

cpu_names = ['cpu%02d' % n for n in range(cpus)]
freq_names = ['freq%02d' % n for n in range(cpus)]
temp_names = ['temp%02d' % n for n in range(temps)]
names = ['d0', 'd1']+cpu_names+freq_names+temp_names

df = pd.read_csv(ifile, sep=" ", header=None, parse_dates={'time': [0,1]}, names=names).set_index('time')

last_recs = df.index > (dt.datetime.now() - dt.timedelta(hours=args.hours))

fig, axes = plt.subplots(nrows=3, ncols=1, sharex='col')
ax0 = df[last_recs].rolling(args.window).mean()[::args.step].plot(y=cpu_names, ax=axes[0], **plot_style)
ax0.set_ylabel('U, %')
ax1 = df[last_recs].rolling(args.window).mean()[::args.step].plot(y=freq_names, ax=axes[1], **plot_style)
ax1.set_ylabel('F, MHz')
ax2 = df[last_recs].rolling(args.window).mean()[::args.step].plot(y=temp_names, ax=axes[2], **plot_style)
ax2.set_ylabel('T, $^O$C')
plt.show()
