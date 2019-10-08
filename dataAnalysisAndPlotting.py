#!/usr/bin/env python

import os
import csv
import re
import matplotlib.pyplot as plt
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    if args == 0:
        print('Please enter the input file name')
        return
    filename = args.filename;

    x = []
    y = []
    # entries = os.listdir('/Users/purnima/PycharmProjects/ITP/KK/')
    # for entry in entries:
    with open(filename, 'rb') as f:
        data = f.read()
        pos = data.find(b"CellGamma \n   20000")
        data = data[pos + 11:].split(b'\n')
        first_line = data[0].decode('utf-8').split()

        pzz_initial = float(first_line[10])
        lz_initial = float(first_line[16])

        with open('/Users/purnima/PycharmProjects/ITP/KK/PzzLz.csv', 'a') as csvFile:
            my_fields = ['Stress', 'Strain']
            writer = csv.DictWriter(csvFile, fieldnames=my_fields)
            writer.writeheader()

            for datum in data[1:]:
                datum = datum.decode('utf-8')
                if re.match('[a-zA-Z]+', datum) or datum == "":
                    break
                else:
                    individual_datum = datum.split()
                    individual_datum[10] = (float(individual_datum[10]) - pzz_initial) * 0.000101325
                    individual_datum[16] = ((float(individual_datum[16])) - lz_initial) / lz_initial

                    writer.writerow({'Stress': individual_datum[10], 'Strain': individual_datum[16]})

    # Graph
    with open('/Users/purnima/PycharmProjects/ITP/KK/PzzLz.csv', 'r') as csv_file:
        plots = csv.DictReader(csv_file)
        for row in plots:
            y.append(float(row['Stress']))
            x.append(float(row['Strain']))

    fig = plt.figure()
    plt.plot(x, y, label='Loaded from ' + filename)
    plt.xlabel('Strain')
    plt.ylabel('Stress')
    plt.title('Curve')
    plt.legend()
    plt.savefig('/Users/purnima/PycharmProjects/ITP/KK/test.png')
    plt.close(fig)
    plt.show()

    os.remove('PzzLz.csv')


main()
