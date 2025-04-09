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
