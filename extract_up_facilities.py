import osmium
import json
import os

INPUT = "northern-zone-latest.osm.pbf"
OUTPUT = "static/data/up_emergency_facilities.json"

# Same bounds as your UP PMTiles
SOUTH = 23.8
WEST = 77.0
NORTH = 30.5
EAST = 84.7


class FacilityHandler(osmium.SimpleHandler):

    def __init__(self):
        super().__init__()
        self.facilities = []

    def add_facility(self, obj, lat, lon):

        if lat is None or lon is None:
            return

        # Keep only the UP/PMTiles geographic area
        if not (
            SOUTH <= lat <= NORTH
            and WEST <= lon <= EAST
        ):
            return

        tags = obj.tags

        amenity = tags.get("amenity")

        if amenity == "hospital":
            facility_type = "Hospital"
            icon = "🏥"

        elif amenity == "police":
            facility_type = "Police Station"
            icon = "🚓"

        elif amenity == "fire_station":
            facility_type = "Fire Station"
            icon = "🚒"

        else:
            return

        name = tags.get("name", "Unnamed facility")

        self.facilities.append({
            "name": name,
            "type": facility_type,
            "icon": icon,
            "latitude": float(lat),
            "longitude": float(lon)
        })


    def node(self, node):

        if node.location.valid():

            self.add_facility(
                node,
                node.location.lat,
                node.location.lon
            )


    def way(self, way):

        # Ways don't have a direct location.
        # Calculate their approximate center.

        coords = []

        for node in way.nodes:

            if node.location.valid():

                coords.append((
                    node.location.lat,
                    node.location.lon
                ))

        if not coords:
            return

        lat = sum(x[0] for x in coords) / len(coords)
        lon = sum(x[1] for x in coords) / len(coords)

        self.add_facility(
            way,
            lat,
            lon
        )


    def relation(self, relation):

        # Relations are uncommon for these facilities.
        # Ignore them rather than creating inaccurate coordinates.
        return


print()
print("==========================================")
print(" DIVYA AI - UP FACILITY EXTRACTOR")
print("==========================================")
print()

if not os.path.exists(INPUT):

    print("ERROR:")
    print("Could not find:")
    print(INPUT)
    print()

    raise SystemExit(1)


file_size = os.path.getsize(INPUT)

print(
    "PBF size:",
    round(file_size / (1024 * 1024), 2),
    "MB"
)

print()
print("Reading OpenStreetMap data...")
print("This may take a few minutes.")
print()


handler = FacilityHandler()

handler.apply_file(
    INPUT,
    locations=True
)


print()
print("OSM processing complete.")
print(
    "Facilities found:",
    len(handler.facilities)
)


# Remove duplicates

unique = {}

for facility in handler.facilities:

    key = (
        facility["type"],
        round(facility["latitude"], 6),
        round(facility["longitude"], 6)
    )

    unique[key] = facility


facilities = list(unique.values())


# Sort facilities

facilities.sort(
    key=lambda x: (
        x["type"],
        x["name"].lower()
    )
)


# Create final JSON

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

    "facility_count":
        len(facilities),

    "facilities":
        facilities

}


os.makedirs(
    os.path.dirname(OUTPUT),
    exist_ok=True
)


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
print("==========================================")
print(" SUCCESS")
print("==========================================")
print()

print(
    "Total facilities:",
    len(facilities)
)

print()

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
print()