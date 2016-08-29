import json
import googlemaps
import sqlite3
import os
from datetime import datetime

locs = json.loads(open('locations.json', 'r').read())
origin = locs['origin']
destination = locs['destination']

db = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'database.db'))
cursor = db.cursor()

fp = open(os.path.join(os.path.dirname(__file__), 'keys.json'), 'r')
apikey = json.loads(fp.read())["gmaps_distance_matrix_api_key"]

gmaps = googlemaps.Client(key=apikey)
res = gmaps.distance_matrix(
    origins=[origin, destination],
    destinations=[destination, origin],
    mode="driving",
    units="imperial",
    departure_time="now"
)

fromto = res["rows"][0]["elements"][0]
tofrom = res["rows"][1]["elements"][1]

entries = [
    (origin, destination, fromto["duration_in_traffic"]["value"]/60.0, datetime.now().isoformat()),
    (destination, origin, tofrom["duration_in_traffic"]["value"]/60.0, datetime.now().isoformat())
]
cursor.executemany("INSERT INTO durations VALUES (?, ?, ?, ?)", entries)

db.commit()

# for row in cursor.execute("SELECT * FROM durations ORDER BY timestamp LIMIT 2"):
#     print row
print "Done."
