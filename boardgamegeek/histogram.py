import csv
import matplotlib.pyplot as plt
import numpy as np

with open('newTableA.csv', 'r') as csv_in:
    csv_reader = csv.DictReader(csv_in)

    first_row = True
    min_playerss = []
    for row in csv_reader:
        if row['min_players'] != '':
            min_playerss.append(float(row['min_players']))
            if float(row['min_players']) > 5:
                # print(row)
                print(row['name'])
                print(row['min_players'])


    # gaussian_numbers = np.random.randn(1000)
    hist= plt.hist(np.asarray(min_playerss).astype(np.int), bins=range(40), range=(0,40))
    plt.title("Minimum Age Histogram")
    plt.xlabel("Minimum Age")
    plt.ylabel("Frequency")
    plt.show()

    print(hist)
    print(bin_edges)

    # print(max(min_playerss))

