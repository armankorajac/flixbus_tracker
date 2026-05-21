import os
import sys
from pathlib import Path # Path is very nice for handling file paths in a cross-platform way - not to have absolute paths around in the code!

sys.path.append(str(Path().resolve().parent))

RAW_DATA_DIR = Path().resolve().parent / "data" / "raw"

BASE_URL="https://global.api.flixbus.com"


import requests
from config import STATIONS
from config import API_KEY #import the sensitive API_KEY from the config file, which in turn loads it from the .env file
from datetime import datetime, timedelta, timezone
import time

import json


#Flixbus time format is ISO 8601, i.e. this one below, so we need to convert our format to this one
#time_from = "2026-05-07T17:48:00.000Z"
#time_to = "2026-05-07T20:18:00.000Z"


#Function for formatting the time for the flixbus API and for the filenames
def format_time_for_flixbus_api(time):
    timeflix = time.isoformat(timespec="minutes") + ":00.000Z" #get the current time in ISO 8601 format, which is the format required by the FLIXBUS API
    timeflix=timeflix.replace(":", "%3A") #replace the ":" with "%3A" to make it URL safe, as required by the FLIXBUS API
    
    timefile = time.isoformat(timespec="minutes").replace(":", "_").replace("-", "_") #replace the ":" and "-" with "_" to make it a valid filename
    return timeflix, timefile

def get_departures(station_name):

    station_id = STATIONS[station_name]

    #Make it dynamic in time when you call the function 
    now = datetime.now()
    print("Current time: ", now)
    _, time_now_file = format_time_for_flixbus_api(now)
    time_in_4_hours, time_in_4_hours_file = format_time_for_flixbus_api(now + timedelta(hours=4))
    time_before_1_hour, time_before_1_hour_file = format_time_for_flixbus_api(now - timedelta(hours=1))


    url = f"{BASE_URL}/gis/v2/timetable/{station_id}/departures?from={time_before_1_hour}&to={time_in_4_hours}&apiKey={API_KEY}"
    print(url) #print the URL to check if it's correct

    response = requests.get(url)

    response.raise_for_status() #raise an error if the response is not successful

    json_data = response.json() #get the response in JSON format

    json_data["snapshot_time"] = now.isoformat(timespec="seconds")  #add the snapshot time to the JSON data, in ISO 8601 format




    with open(f"{RAW_DATA_DIR}/{station_name}_departures_{time_before_1_hour_file}_to_{time_in_4_hours_file}_snapshotted_{time_now_file}.json", "w") as f:
        json.dump(json_data, f, indent=4)

    


#For now we will not loop through the stations, later on we can
station1 = "genoa_principe"
station2 = 'milan_lampugnano'

while True:

    get_departures(station1)
    get_departures(station2)
    print("Sleeping for 10 minutes...")
    time.sleep(10 * 60) #sleep for 10 minutes before making the next API call

#from 19th of May 15:45 of snapshot time, we have also the snapshot data in the JSON files! 