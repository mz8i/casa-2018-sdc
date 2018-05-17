import os
from dateutil import tz
import pandas as pd

analysis_dir = os.getcwd()
data_dir = os.path.join(analysis_dir, 'data')

sunlight = pd.read_csv(os.path.join(data_dir, 'export_sunlight.csv'))

cols = ['astronomical_twilight_begin', 'astronomical_twilight_end', 'nautical_twilight_begin', 'nautical_twilight_end', 'civil_twilight_begin', 'civil_twilight_end', 'solar_noon', 'sunrise', 'sunset']

sunlight[cols] = sunlight[cols].apply(lambda x: pd.to_datetime(x))

utczone = tz.tzutc()
chicagozone = tz.gettz('US/Central')

print(utczone)
print(chicagozone)

sunlight[cols] = sunlight[cols].applymap(lambda x: x.replace(tzinfo=utczone).astimezone(chicagozone))

sunlight.to_csv(os.path.join(data_dir, 'sunlight_local.csv'))