#!/usr/bin/env python
import os
import sys
import argparse
import datetime as dt

import matplotlib.pyplot as plt
import pandas as pd

parser = argparse.ArgumentParser(description="Plot CPU usage, frequency and temperature")
parser.add_argument('-n', '--hours', type=float, default=2, help='Show plots for the last <n> hours')
parser.add_argument('-w', '--window', type=int, default=3, help='Sliding average over <w> minutes')
parser.add_argument('-s', '--step', type=int, default=1, help='Plot each <s> record')
args = parser.parse_args(sys.argv[1:])

cpus = 32
temps = 4 

plot_style = dict(legend = False)

script_path = os.path.dirname(os.path.realpath(__file__))
ifile = os.path.join(script_path, 'conky.txt')

cpu_names = ['cpu%02d' % n for n in range(cpus)]
freq_names = ['freq%02d' % n for n in range(cpus)]
temp_names = ['temp%02d' % n for n in range(temps)]
names = ['d0', 'd1']+cpu_names+freq_names+temp_names

fig, axes = plt.subplots(nrows=3, ncols=1, sharex='col')

ax0 = None

while True:
    if not ax0 is None:
        ax0.clear()
        ax1.clear()
        ax2.clear()
    df = pd.read_csv(ifile, sep=" ", header=None, parse_dates={'time': [0,1]}, names=names).set_index('time')
    last_recs = df.index > (dt.datetime.now() - dt.timedelta(hours=args.hours))
    df = df[last_recs]

    ax0 = df.rolling(args.window).mean()[::args.step].plot(y=cpu_names, ax=axes[0], **plot_style)
    ax01 = df[cpu_names].mean(axis=1).plot(ax=axes[0], legend=False, ls='-', marker='.', color='k')
    ax0.set_ylabel('U, %')
    ax1 = df.rolling(args.window).mean()[::args.step].plot(y=freq_names, ax=axes[1], **plot_style)
    ax11 = df[freq_names].mean(axis=1).plot(ax=axes[1], legend=False, ls='-', marker='.', color='k')
    ax1.set_ylabel('F, MHz')
    ax2 = df.rolling(args.window).mean()[::args.step].plot(y=temp_names, ax=axes[2], **plot_style)
    ax21 = df[temp_names].mean(axis=1).plot(ax=axes[2], legend=False, ls='-', marker='.', color='k')
    ax2.set_ylabel('T, $^O$C')
    plt.pause(10)

plt.show()
