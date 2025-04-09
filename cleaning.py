import csv
import pandas as pd
import numpy as np
import datetime

import matplotlib.pyplot as plt

from typing import List, Tuple, Dict

def main(fname = "./Data/dataset_mood_smartphone.csv"):
    """
    Main function for testing purposes
    """
    rawSet, users = loadData(fname)
    print(rawSet["screen"][0])

def loadData(fname: str) -> Tuple[pd.DataFrame, List[str]]:
    """
    Loads dataset csv into usable pandas dataframe.

    Args:
        fname: Filepath of the csv File to load in
    
    Returns: A tuple containing the pandas dataframe and the list of user ID's
    """
    with open(fname) as csvFile:
        rawSet = pd.read_csv(csvFile)
    
    # gather user names for easy identification
    users = pd.unique(rawSet["id"]) 

    # Drop unessecary line index
    rawSet.drop("Unnamed: 0", axis="columns", inplace=True) 

    # Convert date/time to datetime objects, to allow for easy temporal resampling
    timeStamps = rawSet["time"].apply(datetime.datetime.fromisoformat)
    rawSet["time"] = timeStamps
    
    # reshape dataset into datapoints ordered by timestamp grouped by user.
    rawSet = pd.pivot_table(rawSet, index=["id" ,"time"], values="value", columns="variable")
    
    return rawSet, users


def resample_hourly(dataframe: pd.DataFrame, users: List[str]) -> pd.DataFrame:
    """
    
    """
    # TODO: - repackage new resampled dataframes into single big dataframe
    #       - determine how to best handle mood per hour
    #       - detect and remove outliers
    for name in users:
        dataframe[name] = dataframe.resample("1h").sum



def resample_dayly(dataframe: pd.DataFrame, users: List[str]) -> pd.DataFrame:
    # TODO: - repackage new resampled dataframes into single big dataframe
    #       - Take sum of times/ scalars and average of reported scores (act, arousal, valence, mood)
    #       - Detect and remove outliers
    
    
    dataframe

if __name__ == "__main__":
    main()