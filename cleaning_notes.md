## Data Cleaning
- **Group data by user**: User data is correlated to the user and comparisons between users at user scale are (likely) invalid.
- **Fill in missing data**: N/a values are to be imputed via two approaches. Low hanging fruit include linear interpolation and stochastic simulation by assuming normal distribution of values. 
    - *What to do in case of prolonged missing data?* 

### Variables and possible impact
- **mood**: The target score to predict, as well as valuable training data
- **circumplex.arousal**: Arousal
- **circumplex.valence**: Attraction to the environment
- **activity**: Activity releases endorphins and is likely to decrease stress and increase mood.
- **screen**: Screentime, given as a start-time and duration. Both holds information over
              total screentime in a day, as well as hidden information like estimated hours of 
              sleep (By taking the longest break in screentime), as well as hours of screentime
              before bed (which could impact quality of sleep.)
- **call**: Telephone calls, some people may become stressed
- **sms**: I become stressed
- **appCat.builtin**: Mundane apps like "Settings" "Camera" and "Flashlight". Low estimated 
                      impact. Might include browser, which makes it more important
- **appCat.communication**: Similar to call and sms; little use could signify lonelyness.
- **appCat.entertainment**: Entertainment usually improves mood in the moment. 
- **appCat.finance**: Money causes stress. Someone that often looks at their finances is either
                      into stocks (rip) or has severe money issues
- **appCat.game**: Gaming improves mood
- **appCat.office**: Mundane. May induce stress from doing filings on smartphone.
- **appCat.other**: No real value, will be highly specific between users.
- **appCat.social**: Social media is a scourge on the human brain.
- **appCat.travel**: Does travel app include maps? If so, includes uneventful if boring morning  
                     commute.
- **appCat.unknown**: No real value
- **appCat.utilities**: Mundanities with low estimated impact.
- **appCat.weather**: Mood impact of weather data relies on weather data we dont have.

### Pruning
- Days that are not followed by a day with moodscores are worthless.
- Days without screen/ app data are worthless, except for mood data.


# TASK 1A: EXPLORATORY DATA ANALYSIS 
- Mood: 
    - Target variable to predict. Days without mood score do not contain the data to properly predict
      mood and can thus be discarded.
    - Mood scores are logged by the user on the hour at semi-random intervals, usually between 1-3 hours
      with long nightly breaks inbetween. Users usually self report around the time they wake up
    - Bias can occur when taking the average reported score of the day since it is uncertain. But also
      mood while sleeping should not be considered an option. Some days only have few datapoints, but 5 on average.
- Arousal & Valence:
    - Two self reported values that respectively hint at internal and external factors in the formation
      of the mood score. 
    - Is self reported with mood, and both suffer from the same drawbacks.

- Activity:
    - Automatically logged activity score, which logs a relative activity score every hour on the hour.
    - Missing activity scores hint at the phone being turned off at the time of logging, supported by missing screen logging.
      measurements.
      - Somehow, scores can still be logged with the phone off
    - Missing scores can not always simply be replaced with 0, unless at night.
  
- Screen & appCat:
    - Logs the starting time and duration of a screentime/ app session. Screen is approximately
     equal to the sum of appcat.
    - Missing values represent the absense ofscreentime and can be taken as 0.
    - When resampling into hours it should be considered whether time overflows into the next hour.
    - When resampling into days, overflowing time can still be considered part of the previous day, but may bring bias for users with structural delayed ciarcadian rhythms.
    - Overly long app usage may indicate a user has fallen asleep
    - Different app types may directly correlate with a user's mood, some are too broad to corectly
      categorize

- Call & Sms:
    - Logs whether a Call or SMS has been sent. 
    - Missing values can be considered the absence of and thus 0.