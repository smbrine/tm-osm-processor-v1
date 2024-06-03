from tools import MathTools

import aiohttp


class OSMTools:
    def __init__(self):
        self.api_url = "http://overpass-api.de/api/interpreter"

    async def fetch_locations(
        self, amenity, lat, lon, radius=1000
    ):
        if amenity == "subway":
            tags = [
                f'node["railway"="station"]["station"="subway"](around:{radius},{lat},{lon});',
            ]
        elif amenity in [
            "school",
            "supermarket",
            "kindergarten",
            "parking",
        ]:
            tags = [
                f'node["amenity" = "{amenity}"](around:{radius}, {lat}, {lon});',
                f'node["building" = "{amenity}"](around:{radius}, {lat}, {lon});',
                f'relation["amenity" = "{amenity}"](around:{radius}, {lat}, {lon});',
                f'relation["building" = "{amenity}"](around:{radius}, {lat}, {lon});',
                f'way["amenity" = "{amenity}"](around:{radius}, {lat}, {lon});',
                f'way["building" = "{amenity}"](around:{radius}, {lat}, {lon});',
            ]
        else:
            tags = [
                f'node["amenity" = "{amenity}"](around:{radius}, {lat}, {lon});',
                f'node["building" = "{amenity}"](around:{radius}, {lat}, {lon});',
                f'relation["amenity" = "{amenity}"](around:{radius}, {lat}, {lon});',
                f'relation["building" = "{amenity}"](around:{radius}, {lat}, {lon});',
                f'way["amenity" = "{amenity}"](around:{radius}, {lat}, {lon});',
                f'way["building" = "{amenity}"](around:{radius}, {lat}, {lon});',
            ]

        query = f"""
           [out:json];
           (
             {''.join(tags)}
           );
           out center;
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.api_url,
                params={"data": query},
            ) as response:
                response.raise_for_status()
                return await response.json()

    def calculate_distance(self, coord1, coord2):
        return MathTools.haversine(
            coord1[0],
            coord1[1],
            coord2[0],
            coord2[1],
        )

    async def find_nearest_object(
        self, amenity, lat, lon, radius=1000
    ):
        amenities = await self.fetch_locations(
            amenity, lat, lon, radius
        )
        nearest_object = None
        min_distance = float("inf")
        current_location = (lat, lon)

        for obj in amenities.get("elements", []):
            try:
                obj_coords = (
                    obj["lat"],
                    obj["lon"],
                )
            except KeyError:
                obj_coords = (
                    obj["center"]["lat"],
                    obj["center"]["lon"],
                )
            distance = self.calculate_distance(
                current_location, obj_coords
            )
            if distance < min_distance:
                min_distance = distance
                nearest_object = obj
                nearest_object["distance"] = (
                    min_distance  # Adding distance in meters
                )

        return nearest_object


# Usage
if __name__ == "__main__":
    tools = OSMTools()
    test_lat = 55.893996
    test_lon = 37.392097

    nearest_school = tools.find_nearest_object(
        "school", test_lat, test_lon, 1000
    )
    nearest_subway = tools.find_nearest_object(
        "subway", test_lat, test_lon, 1000
    )
    nearest_supermarket = (
        tools.find_nearest_object(
            "supermarket",
            test_lat,
            test_lon,
            1000,
        )
    )
    nearest_kindergarten = (
        tools.find_nearest_object(
            "kindergarten",
            test_lat,
            test_lon,
            1000,
        )
    )
    nearest_parking = tools.find_nearest_object(
        "parking", test_lat, test_lon, 1000
    )

    if nearest_school:
        print(
            f"Nearest school information: {nearest_school['tags']}"
        )
        print(
            f"Distance to nearest school: {nearest_school['distance']:.2f} meters"
        )
    else:
        print(
            "No schools found within the specified radius."
        )

    if nearest_subway:
        print(
            f"Nearest subway information: {nearest_subway}"
        )
        print(
            f"Distance to nearest subway: {nearest_subway['distance']:.2f} meters"
        )
    else:
        print(
            "No subway station found within the specified radius."
        )

    if nearest_supermarket:
        print(
            f"Nearest supermarket information: {nearest_supermarket['tags']}"
        )
        print(
            f"Distance to nearest supermarket: {nearest_supermarket['distance']:.2f} meters"
        )
    else:
        print(
            "No subway station found within the specified radius."
        )

    if nearest_kindergarten:
        print(
            f"Nearest kindergarten information: {nearest_kindergarten['tags']}"
        )
        print(
            f"Distance to nearest kindergarten: {nearest_kindergarten['distance']:.2f} meters"
        )
    else:
        print(
            "No kindergarten found within the specified radius."
        )

    if nearest_parking:
        print(
            f"Nearest parking information: {nearest_parking['tags']}"
        )
        print(
            f"Distance to nearest parking: {nearest_parking['distance']:.2f} meters"
        )
    else:
        print(
            "No parking found within the specified radius."
        )
