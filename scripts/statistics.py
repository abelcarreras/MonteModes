#!/usr/bin/env python

import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Statistics options')

parser.add_argument('data_file', metavar='data_file', type=str,
                    help='input file data in columns')

parser.add_argument('-c', '--column', metavar='c', type=int, default=0,
                   help='column data')

parser.add_argument('-r', '--relaxation', metavar='r', type=int, default=0,
                   help='relaxation steps')

parser.add_argument('-o', '--output_file', metavar='r', type=str, default=None,
                   help='store data in output file')

parser.add_argument('-p', action='store_true',
                   help='plot data (requires matplotlib)')


args = parser.parse_args()

filename = args.data_file

column = args.column-1
relaxation_steps = args.relaxation

data = np.loadtxt(filename,dtype=float)
#data = np.random.rand(1,10000000)

#Check input data
if (column >= data.shape[1]):
    print ('Column error, check input file format')
    exit()

if (relaxation_steps >= data.shape[0]):
    print ('Too much relaxation steps, not enough data')
    exit()


data = data[relaxation_steps:, column]

print ('Number of data (after relaxation steps): {}'.format(len(data)))

#Histogram
histogram = np.histogram(data, density=True, bins=300)
hist_frequencies= histogram[0]
bin_ranges = histogram[1]
bin_centers = bin_ranges[:-1] + np.diff(bin_ranges) / 2

#Average & deviation

average = np.average(data)
std_deviation = np.std(data)

print ('Average: {}\nStandard deviation: {}'.format(average,std_deviation))

#Plot histogram data
if args.p:
    import matplotlib.pyplot as plt
    plt.plot(bin_centers, hist_frequencies)
    plt.show()
if args.output_file:
    f = open(args.output_file, mode='w+')
    f.writelines('#      Bin center           Frequency\n')
    for x, y in zip(bin_centers,hist_frequencies):
        f.writelines('{0:20f} {1:20f} \n'.format(x, y))
else:
    print ('#      Bin center           Frequency')
    for x, y in zip(bin_centers,hist_frequencies):
        print ('{0:20f} {1:20f}'.format(x, y))