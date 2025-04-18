import pandas as pd
import numpy as np
import datetime

import copy

import cleaning

from typing import List, Tuple, Dict

def main():
    rawData, users = cleaning.loadData("./Data/dataset_mood_smartphone.csv")
    print(reinstanceDataset(rawData, users))

def reinstanceDataset(df: pd.DataFrame, users: List[str], period=5) -> pd.DataFrame:
    """
    Reinstancing function that converts the time-seried userstats of the dataframe into a series
    of time averaged "sub-users", indexed by user[str] and "sub-user"[int]. 
    
    Sub users contain all variables of the original users, with the following alterations:
        - All time (eg. screen and appcat) variables represent the mean cumulative time per day.
        - Call and SMS are the mean cumulative per day as well
        - A new column called "nextday" has been added that contains the mean mood of the following day.
        - Activity is the average daily activity defined as the sum of activities per day / 16 (eg. waking hours)
        - All remaining variables are the averaged values over time.

    The function seeks out all possible date-ranges of uninterrupted "activity" and "mood" data, defined
    as at least one mood score per day and at least 10 activity points per day, as well as a non-zero
    mean activity. The reason for this is because activity is a good indicator for how much the the phone
    was on over the course of the day (eg. nan activity usually coincided with nan screentime in hourly-resampled sets.)

    Args:
        df: Dataframe of all raw user statistics
        users: List of all usernames.
        period: period in days to take average from.
    
    Returns: The instance based dataset.

    """
    timeCorrected = cleaning.remove_useTimeOutliers(df)
    byDay           = cleaning.resample_daily(df, users)

    dates         = cleaning.find_measuredDays(timeCorrected, users)
    subUsers = []

    subKeys = []
    for user in users:
        subUser = genSubUsers(df.loc[user], byDay.loc[user], dates[user], period)

        if subUser is None: 
            print(user, " cannot provide subusers in ranges")
            continue

        subUsers.append(subUser)
        subKeys.append(user)

    reinstanced = pd.concat(subUsers, keys=subKeys)
    
    return reinstanced


def genSubUsers(userFrame: pd.DataFrame, resampledUser: pd.DataFrame, 
                dateRanges: List[Tuple[datetime.datetime, datetime.datetime]], period: int) -> List[pd.DataFrame]:
    """
    Generates a reinstanced "sub-user" for a single user, between all dateranges associated with the user.

    Args:
        userFrame: Time-seried data of the user
        resampledUser: Data from the user corresponding to the "daily resampling" function in cleaning
        dateRanges: A list of [start and end] dates signifying unbroken Activity & mood logging.
        period: The time period in days.
    """
    DAY = datetime.timedelta(1)
    timeKeys = ["screen"] + [index for index in userFrame.columns if "appCat" in index]

    subUsers = []
    for dRange in dateRanges:
        timespan = dRange[1] - dRange[0]
        if timespan.days < period + 1:
            continue
        
        startDate, endDate = dRange[0], dRange[0] + datetime.timedelta(period)
        while endDate < dRange[1]:
            subUser  = userFrame.loc[startDate:endDate].mean()

            subUser[timeKeys] = resampledUser[timeKeys].loc[startDate:endDate].mean()

            subUser["sms"] =  resampledUser["sms"].loc[startDate:endDate].mean()
            subUser["call"] =  resampledUser["call"].loc[startDate:endDate].mean()
            subUser["activity"] =  resampledUser["activity"].loc[startDate:endDate].mean()

            subUser["nextday"] = userFrame["mood"].loc[endDate:endDate + DAY].mean()
            subUsers.append(subUser)


            startDate = startDate + DAY
            endDate   = endDate   + DAY
    if not subUsers:
        return None
    out = pd.concat(subUsers, axis=1, keys = list(range(len(subUsers)))).transpose()

    return out

if __name__ == "__main__":
    main()