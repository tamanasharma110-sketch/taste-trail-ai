import googlemaps
from geopy.distance import geodesic
import streamlit as st


class TasteTrailAgent:

    def __init__(self):

        self.gmaps = googlemaps.Client(
            key=st.secrets["GOOGLE_API_KEY"]
        )

    def get_coords(self, location):

        try:
            geo = self.gmaps.geocode(location)
            if not geo:
                return None

            loc = geo[0]["geometry"]["location"]
            return (loc["lat"], loc["lng"])

        except Exception:
            return None

    # 🔥 Get REAL Google reviews
    def get_reviews(self, place_id):

        try:
            details = self.gmaps.place(
                place_id=place_id,
                fields=["name", "rating", "reviews"]
            )

            reviews = details.get("result", {}).get("reviews", [])

            formatted_reviews = []

            for r in reviews[:3]:  # top 3 reviews only
                text = r.get("text", "")
                author = r.get("author_name", "User")

                formatted_reviews.append({
                    "author": author,
                    "text": text
                })

            return formatted_reviews

        except Exception:
            return []

    def run(self, dish, location):

        user_loc = self.get_coords(location)

        if not user_loc:
            return []

        try:
            places = self.gmaps.places_nearby(
                location=user_loc,
                radius=5000,
                keyword=dish,
                type="restaurant"
            ).get("results", [])
        except Exception:
            return []

        results = []

        for p in places:

            name = p.get("name", "Unknown")
            rating = p.get("rating", 0)
            place_id = p.get("place_id")

            loc = p["geometry"]["location"]

            distance = geodesic(
                user_loc,
                (loc["lat"], loc["lng"])
            ).km

            # AI-style ranking (simple + explainable)
            score = (rating * 2) - (distance * 0.3)

            reviews = self.get_reviews(place_id)

            results.append({
                "name": name,
                "rating": rating,
                "distance_km": round(distance, 2),
                "score": round(score, 2),
                "reviews": reviews
            })

        return sorted(results, key=lambda x: x["score"], reverse=True)