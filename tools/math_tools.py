import math


class MathTools:
    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        """Calculate the great circle distance in kilometers between two points
        on the earth (specified in decimal degrees)
        """
        # Convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(
            math.radians, [lon1, lat1, lon2, lat2]
        )

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1)
            * math.cos(lat2)
            * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(
            math.sqrt(a), math.sqrt(1 - a)
        )
        r = 6371  # Radius of earth in kilometers
        return c * r * 1000
