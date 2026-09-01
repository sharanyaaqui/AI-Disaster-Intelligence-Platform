import requests
import json
from pathlib import Path
import time

SOUTH = 23.8
WEST = 77.0
NORTH = 30.5
EAST = 84.7

# Try multiple Overpass servers
OVERPASS_SERVERS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter"
]

OUTPUT_FILE = Path(
    "static/data/up_emergency_facilities.json"
)

query = f"""
[out:json][timeout:600];

(
  nwr["amenity"="hospital"]({SOUTH},{WEST},{NORTH},{EAST});
  nwr["amenity"="police"]({SOUTH},{WEST},{NORTH},{EAST});
  nwr["amenity"="fire_station"]({SOUTH},{WEST},{NORTH},{EAST});
);

out center tags;
"""

print("==========================================")
print(" DIVYA AI - UP FACILITY DOWNLOADER")
print("==========================================")
print()
print("Downloading emergency facilities for")
print("Uttar Pradesh...")
print()
print("Please wait. This can take several minutes.")
print()

data = None

for server in OVERPASS_SERVERS:

    print("Trying:")
    print(server)
    print()

    try:

        response = requests.post(
            server,
            data={"data": query},
            timeout=900
        )

        print(
            "HTTP status:",
            response.status_code
        )

        response.raise_for_status()

        data = response.json()

        print("Download successful!")
        print()

        break

    except Exception as error:

        print("This server failed:")
        print(error)
        print()

        time.sleep(2)


if data is None:

    print("==========================================")
    print(" DOWNLOAD FAILED")
    print("==========================================")
    print()
    print("All Overpass servers failed.")
    print()
    print("This is usually a temporary network/server")
    print("problem, not a problem with your project.")
    print()

    raise SystemExit(1)


facilities = []

for element in data.get("elements", []):

    tags = element.get("tags", {})

    amenity = tags.get("amenity")

    if amenity not in [
        "hospital",
        "police",
        "fire_station"
    ]:
        continue

    latitude = element.get("lat")
    longitude = element.get("lon")

    if latitude is None and element.get("center"):

        latitude = element["center"].get("lat")
        longitude = element["center"].get("lon")

    if latitude is None or longitude is None:
        continue

    if amenity == "hospital":

        facility_type = "Hospital"
        icon = "🏥"

    elif amenity == "police":

        facility_type = "Police Station"
        icon = "🚓"

    else:

        facility_type = "Fire Station"
        icon = "🚒"

    facilities.append({

        "id":
            f"{element.get('type')}_{element.get('id')}",

        "name":
            tags.get(
                "name",
                "Unnamed facility"
            ),

        "type":
            facility_type,

        "icon":
            icon,

        "latitude":
            latitude,

        "longitude":
            longitude,

        "phone":
            tags.get("phone", ""),

        "address":
            tags.get("addr:street", "")

    })


# Remove duplicates

unique = {}

for facility in facilities:

    unique[facility["id"]] = facility


facilities = list(
    unique.values()
)


output = {

    "region":
        "Uttar Pradesh",

    "bounds": {

        "south":
            SOUTH,

        "west":
            WEST,

        "north":
            NORTH,

        "east":
            EAST

    },

    "source":
        "OpenStreetMap / Overpass API",

    "facility_count":
        len(facilities),

    "facilities":
        facilities

}


OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        output,
        file,
        ensure_ascii=False,
        indent=2
    )


hospitals = sum(
    1
    for f in facilities
    if f["type"] == "Hospital"
)

police = sum(
    1
    for f in facilities
    if f["type"] == "Police Station"
)

fire = sum(
    1
    for f in facilities
    if f["type"] == "Fire Station"
)


print("==========================================")
print(" DOWNLOAD COMPLETE")
print("==========================================")
print()
print(
    "Total facilities:",
    len(facilities)
)
print()
print(
    "Hospitals:",
    hospitals
)
print(
    "Police stations:",
    police
)
print(
    "Fire stations:",
    fire
)
print()
print(
    "Saved to:"
)
print(
    OUTPUT_FILE
)