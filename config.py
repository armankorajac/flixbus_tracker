import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FLIXBUS_API_KEY")

#The unique IDs of the stations that we want to track.
#Note that in the files the stations, buses and routes are identified by unique IDs. 

STATIONS = {
    "genoa_principe": "dcc02ea8-9603-11e6-9066-549f350fcb0c",
    "pisa_pietrasantina": "dcc1a1c8-9603-11e6-9066-549f350fcb0c",
    "trieste_autostazione": "dcbda963-9603-11e6-9066-549f350fcb0c",
    "milan_lampugnano": "dcbc484a-9603-11e6-9066-549f350fcb0c",
    "napoli_centrale": "dcc19a38-9603-11e6-9066-549f350fcb0c",
}