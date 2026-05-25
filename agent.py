import googlemaps
from geopy.distance import geodesic
import streamlit as st
import google.generativeai as genai


class TasteTrailAgent:

    def __init__(self):

        # Google Maps
        self.gmaps = googlemaps.Client(
            key=st.secrets["GOOGLE_API_KEY"]
        )

        # Gemini AI
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel("gemini-1.5-flash")

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

        # Step 1: build base list
        for p in places:

            name = p.get("name", "Unknown")
            rating = p.get("rating", 0)

            loc = p["geometry"]["location"]

            distance = geodesic(
                user_loc,
                (loc["lat"], loc["lng"])
            ).km

            ai_score = (rating * 2) - (distance * 0.3)

            results.append({
                "name": name,
                "rating": rating,
                "distance_km": round(distance, 2),
                "ai_score": round(ai_score, 2)
            })

        # Step 2: sort results
        results = sorted(results, key=lambda x: x["ai_score"], reverse=True)

        # Step 3: take TOP 3 for Gemini
        top_results = results[:3]

        # Step 4: Gemini explanation (ONLY ONCE)
        prompt = f"""
You are a professional food critic AI.

User searched for: {dish}

Here are the top restaurant options:
{top_results}

Give:
1. Best restaurant recommendation
2. Why it is the best (simple explanation)
3. One-line suggestion for user

Keep it short and human-like.
"""

        ai_review = self.model.generate_content(prompt).text

        return {
            "results": results,
            "ai_review": ai_review
        }