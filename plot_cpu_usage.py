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
csv_names = ['d0', 'd1']+cpu_names+freq_names+temp_names

fig, axes = plt.subplots(nrows=3, ncols=1, sharex='col')

plots = []

labels = ['U, %', 'F, MHz', 'T, $^O$C']
names = [cpu_names, freq_names, temp_names]

while True:
    for plot in plots:
         plot.clear()
    df = pd.read_csv(ifile, sep=" ", header=None, parse_dates={'time': [0,1]}, names=csv_names).set_index('time')
    last_recs = df.index > (dt.datetime.now() - dt.timedelta(hours=args.hours))
    df = df[last_recs].rolling(args.window).median()[::args.step]

    plots = []
    for l, n, a in zip(labels, names, axes):
        plots.append(df[n].plot(ax=a, **plot_style))
        plots.append(df[n].mean(axis=1).plot(ax=a, legend=False, ls='-', marker='.', color='k'))
        plots[-1].set_ylabel(l)

    plt.pause(10)

plt.show()
