import googlemaps
from geopy.distance import geodesic
import streamlit as st


class TasteTrailAgent:

    def __init__(self):

        # FIXED STREAMLIT SECRET USAGE
        self.gmaps = googlemaps.Client(
            key=st.secrets["AIzaSyCtA_07Sq9GkxNCd8ZsGVgSPPKcFVJyFqg"]
        )

    def get_coords(self, location):

        geo = self.gmaps.geocode(location)

        if not geo:
            return None

        loc = geo[0]["geometry"]["location"]

        return (loc["lat"], loc["lng"])

    def run(self, dish, location):

        user_loc = self.get_coords(location)

        if not user_loc:
            return []

        places = self.gmaps.places_nearby(
            location=user_loc,
            radius=5000,
            keyword=dish,
            type="restaurant"
        ).get("results", [])

        results = []

        for p in places:

            name = p.get("name", "Unknown")
            rating = p.get("rating", 0)

            loc = p["geometry"]["location"]

            distance = geodesic(
                user_loc,
                (loc["lat"], loc["lng"])
            ).km

            # AI ranking formula
            ai_score = (rating * 2) - (distance * 0.3)

            results.append({
                "name": name,
                "rating": rating,
                "distance_km": round(distance, 2),
                "ai_score": round(ai_score, 2)
            })

        return sorted(results, key=lambda x: x["ai_score"], reverse=True)