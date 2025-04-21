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


def predict_mood(fname="./Data/dataset_mood_smartphone.csv"):
    with open(fname) as csvFile:
        rawSet = pandas.read_csv(csvFile)
    mood_data = rawSet.loc[rawSet["variable"] == "mood"]
    mood_data["datetime"] = pandas.to_datetime(mood_data["time"])
    mood_data = mood_data.sort_values(by=["id", "datetime"])
    
    predictions = {}
    for user in pandas.unique(mood_data["id"]):
        user_data = mood_data[mood_data["id"] == user]
        if len(user_data) > 1:
            last_mood = user_data.iloc[-2]["value"]
            predictions[user] = last_mood
        else:
            predictions[user] = "Not enough data"
    
    print("Mood Predictions:")
    for user, prediction in predictions.items():
        print(f"User {user}: {prediction}")


predict_mood()