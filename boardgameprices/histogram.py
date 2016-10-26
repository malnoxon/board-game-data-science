import csv
import matplotlib.pyplot as plt
import numpy as np

with open('new_tableA.csv', 'r') as csv_in:
    csv_reader = csv.DictReader(csv_in)

    first_row = True
    years = []
    for row in csv_reader:
        years.append(row['year'])

    print(years)
    gaussian_numbers = np.random.randn(1000)
    plt.hist(years)
    plt.title("Gaussian Histogram")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.show()


