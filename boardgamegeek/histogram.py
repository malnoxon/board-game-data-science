import csv
import matplotlib.pyplot as plt
import numpy as np

with open('newTableA.csv', 'r') as csv_in:
    csv_reader = csv.DictReader(csv_in)

    first_row = True
    min_ages = []
    for row in csv_reader:
        if row['min_age'] != '':
            min_ages.append(float(row['min_age']))
            if float(row['min_age']) < 2:
                # print(row)
                print(row['name'])
                print(row['min_age'])


    # gaussian_numbers = np.random.randn(1000)
    hist= plt.hist(np.asarray(min_ages).astype(np.int), bins=range(40), range=(0,40))
    plt.title("Minimum Age Histogram")
    plt.xlabel("Minimum Age")
    plt.ylabel("Frequency")
    plt.show()

    print(hist)
    print(bin_edges)

    # print(max(min_ages))

