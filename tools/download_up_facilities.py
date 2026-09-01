import json
import requests
import time

SOUTH = 23.8
WEST = 77.0
NORTH = 30.5
EAST = 84.7

OUTPUT = "static/data/up_emergency_facilities.json"

ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter"
]

FACILITY_TYPES = [
    ("hospital", "Hospital", "🏥"),
    ("police", "Police Station", "🚓"),
    ("fire_station", "Fire Station", "🚒")
]


def download_facilities(amenity):

    query = f"""
    [out:json][timeout:600];

    nwr["amenity"="{amenity}"]
    ({SOUTH},{WEST},{NORTH},{EAST});

    out center tags;
    """

    for endpoint in ENDPOINTS:

        print()
        print("Trying:", endpoint)
        print("Downloading:", amenity)

        try:

            response = requests.post(
    endpoint,
    data={"data": query},
    headers={
        "User-Agent": "DIVYA-AI/1.0 emergency mapping project"
    },
    timeout=700
)

            print("HTTP status:", response.status_code)

            response.raise_for_status()

            data = response.json()

            print(
                "Downloaded",
                len(data.get("elements", [])),
                amenity,
                "records"
            )

            return data.get("elements", [])

        except Exception as error:

            print("Failed:", error)

            time.sleep(2)

    return None


facilities = []


for amenity, facility_type, icon in FACILITY_TYPES:

    elements = download_facilities(amenity)

    if elements is None:

        print()
        print("Could not download:", facility_type)
        print("Stopping.")
        raise SystemExit(1)

    for element in elements:

        latitude = element.get("lat")
        longitude = element.get("lon")

        if latitude is None and element.get("center"):

            latitude = element["center"].get("lat")
            longitude = element["center"].get("lon")

        if latitude is None or longitude is None:
            continue

        tags = element.get("tags", {})

        name = tags.get(
            "name",
            "Unnamed facility"
        )

        facilities.append({
            "name": name,
            "type": facility_type,
            "icon": icon,
            "latitude": latitude,
            "longitude": longitude
        })


# Remove duplicate facilities

unique = {}

for facility in facilities:

    key = (
        facility["type"],
        round(facility["latitude"], 6),
        round(facility["longitude"], 6)
    )

    unique[key] = facility


facilities = list(unique.values())


facilities.sort(
    key=lambda x: (
        x["type"],
        x["name"].lower()
    )
)


output = {

    "state": "Uttar Pradesh",

    "version": "2.0",

    "source": "OpenStreetMap",

    "bounds": {
        "south": SOUTH,
        "west": WEST,
        "north": NORTH,
        "east": EAST
    },

    "facility_count": len(facilities),

    "facilities": facilities
}


with open(
    OUTPUT,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        output,
        file,
        ensure_ascii=False,
        indent=2
    )


print()
print("======================================")
print("SUCCESS")
print("======================================")

print(
    "Total facilities:",
    len(facilities)
)

for facility_type in [
    "Hospital",
    "Police Station",
    "Fire Station"
]:

    count = sum(
        1
        for f in facilities
        if f["type"] == facility_type
    )

    print(
        facility_type + ":",
        count
    )

print()
print("Saved to:")
print(OUTPUT)