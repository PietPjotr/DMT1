import csv
import pandas

import matplotlib.pyplot as plt

def main(fname = "./Data/dataset_mood_smartphone.csv"):
    with open(fname) as csvFile:
        rawSet = pandas.read_csv(csvFile)
    users = pandas.unique(rawSet["id"])

    print(rawSet.loc[(rawSet["variable"] == "mood") & (rawSet["id"] == users[0])]["value"])
    plot = pandas.plotting.boxplot(rawSet.loc[(rawSet["variable"] == "mood") & (rawSet["id"] == users[0])]["value"])
    plt.show()

def CSV_approach(csvFile):
    reader = csv.DictReader(csvFile)
    for line in reader:
        users = [line["id"] for line in reader]
        print(users)



if __name__ == "__main__":
    main()
