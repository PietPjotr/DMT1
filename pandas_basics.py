import csv
import pandas
import matplotlib.pyplot as plt


def main(fname = "./Data/dataset_mood_smartphone.csv"):
    with open(fname) as csvFile:
        rawSet = pandas.read_csv(csvFile)
    users = pandas.unique(rawSet["id"])
    variables = pandas.unique(rawSet["variable"])
    [print(k, v) for k, v in enumerate(variables)]

    plot = pandas.plotting.boxplot(rawSet.loc[(rawSet["variable"] == variables[4]) & (rawSet["id"] == users[0])]["value"])
    plt.show()


def CSV_approach(csvFile):
    reader = csv.DictReader(csvFile)
    for line in reader:
        users = [line["id"] for line in reader]
        print(users)


if __name__ == "__main__":
    main()


"""
screen is waarschijnlijk de hoeveelheid seconden van scherm aan staan vanaf
het moment dat de timestamp begint.
"""
"""
structuur:

{
    userid1: {class1: [[time], [value]], class2: [[time], [value]], ...
    userid2: ...
    ...
}

"""