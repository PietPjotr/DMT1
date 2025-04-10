import csv
import pandas as pd
import numpy as np
import datetime

import copy

import matplotlib.pyplot as plt

from typing import List, Tuple, Dict

def main(fname = "./Data/dataset_mood_smartphone.csv"):
    """
    Main function for testing purposes
    """
    rawSet, users = loadData(fname)
    
    prunedSet = pruneDays(rawSet, users)
    print(prunedSet)
    print(resample_daily(prunedSet, users))


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

def pruneDays(df: pd.DataFrame, users: List[str], method = "allMood", baseFrame: pd.DataFrame=None) -> pd.DataFrame:
    """
    Data pruning function selector, for convienicence.

    Args:
        df:     dataframe
        users:  userlist
        method: ["allMood", "longest", "longestInc"] (case insensitive)
                allMood: keep all days and only days with mood scores
                longest: Keep the longest series of days with mood scores
                longestInc: Keep all days with mood scores
        baseframe: Optional base dataframe to use in case mood has a generated value from the resampling method.
    """
    if baseFrame is None:
        baseFrame = df
    dateRanges = find_measuredDays(baseFrame, users)

    if method.lower() == "allmood":
        # Create a new frame with all days containing mood scores
        return pruneDays_allMood(df, users, dateRanges)

    if method.lower() == "longest":
        # Create a new frame with the longest streak of days with moodscore
        return pruneDays_longest(df, users, dateRanges, inclusive = False)
    
    if method.lower() == "longestinc":
        # Create a new frame with the longest streak of days and the preceding day.
        return pruneDays_longest(df, users, dateRanges, inclusive = True)


def pruneDays_allMood(df: pd.DataFrame, users: List[str], 
                      dateRanges: Dict[str,Tuple[datetime.datetime,datetime.datetime]]) -> pd.DataFrame:
    """
    Returns a dataset containing data from all days with recorded moodscores.

    Args:
        df:     dataframe
        users:  userlist
        dateRanges: Dictionary of tuples keyed by userIds that represent the date ranges with mood scores.
    """
    outFrames = []

    for user in users:
        # Create a list of dataframes for all dateranges
        pruned_userList = [df.loc[user].loc[date_a:date_b].copy() for date_a, date_b in dateRanges[user]]
        pruned_user = pd.concat(pruned_userList)

        outFrames.append(pruned_user)
    
    return pd.concat(outFrames, keys=users)


def pruneDays_longest(df: pd.DataFrame, users: List[str], 
                      dateRanges: Dict[str,List[Tuple[datetime.datetime,datetime.datetime]]], 
                      inclusive = False,) -> pd.DataFrame:
    """
    Returns a dataset containing data from all days with recorded moodscores from the longest uninterrupted
    series.

    Args:
        df:     dataframe
        users:  userlist
        dateRanges: Dictionary of tuples keyed by userIds that represent the date ranges with mood scores.
        inclusive:  If True, the day before the longest range of mood scores is included 
    """
    outFrames = []

    for user in users:
        dateRange = longestRange(dateRanges[user])
        if inclusive:
            dateRange = (dateRange[0] - datetime.timedelta(days=1), dateRange[1])

        pruned_user = df.loc[user].loc[dateRange[0]:dateRange[1]]
        outFrames.append(pruned_user)
    
    return pd.concat(outFrames, keys=users)

def longestRange(dateRanges: List[Tuple[datetime.datetime,datetime.datetime]]):
    """
    Finds the longest daterange in a list of daterange tuples.
    """
    longest    = 0
    best_index = 0
    for i, (start, end) in enumerate(dateRanges):
        delta = end - start

        if delta.days > longest:
            best_index = i
            longest = delta.days
    
    return dateRanges[best_index]

def find_measuredDays(df: pd.DataFrame, users: List[str]) -> Dict[str, list[Tuple[datetime.date, datetime.date]]]:
    """
    Returns a dictionary of lists of start and end dates of mood measurement periods keyed by userID.
    """
    measureDays_out = dict()

    for user in users:
        # Find all dates with mood activity
        userFrame = df.loc[user].resample("1d").sum() # Sum used since content is irrelevant
        dates = userFrame.loc[userFrame["mood"] > 0].index

        rangeStart = None

        rangeList: List[Tuple[datetime.date, datetime.date]] = []
        rangeStart = dates[0]
        for i, date in enumerate(dates):
            if i == 0: continue
            diff = date - dates[i-1]
            assert isinstance(diff, datetime.timedelta) # To keep my vscode instance happy
            
            if diff.days > 1: # If there is a gap of longer than one day, there must be a new range.
                rangeList.append((copy.copy(rangeStart), copy.copy(dates[i-1])))
                rangeStart = date
        
        rangeList.append((copy.copy(rangeStart), copy.copy(dates[-1])))
        measureDays_out[user] = rangeList

    return measureDays_out


def resample_daily(df: pd.DataFrame, users: List[str]) -> pd.DataFrame:
    """
    Resamples the dataset to a consistent daily format rather than inconsistent timing. Times and calls 
    are summed, subjective scores are average 
    """
    # TODO:
    #       - Detect and remove outliers

    # Generate agg function profile (For resampler)
    sumKeys = [key for key in df.keys() if "appCat" in key]
    sumKeys.append("screen")
    sumKeys.append("sms")
    sumKeys.append("call")
    meanKeys = [key for key in df.keys() if key not in sumKeys]

    sumDict  = {key: "sum" for key in sumKeys}
    meanDict = {key: "mean" for key in meanKeys}
    aggDict  = sumDict | meanDict

    subFrames = []

    for user in users:
        userFrame = df.loc[user].resample("1d").agg(aggDict)
        subFrames.append(userFrame)
    

    outFrame = pd.concat(subFrames, keys=users)
    outFrame["activity"] = outFrame["activity"].fillna(0)
    return outFrame


def resample_hourly(df: pd.DataFrame, users: List[str]) -> pd.DataFrame:
    """
    Resamples the dataset to a consistent hourly format rather than inconsistent timing.
    """
    # TODO: - Determine how to best handle non-subjective variables per hour
    #       - Handle time overflow.
    #       - detect and remove outliers

    aggDict = {key: "sum" for key in df.keys()}

    subFrames = []

    for user in users:
        userFrame = df.loc[user].resample("1h").agg(aggDict)
        subFrames.append(userFrame)
    
    outFrame = pd.concat(subFrames, keys=users)
    return outFrame


if __name__ == "__main__":
    main()