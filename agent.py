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

        # Gemini AI (SAFE CONFIG)
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

        # ⚠️ IMPORTANT: use stable model to avoid NotFound error
        self.model = genai.GenerativeModel("gemini-pro")

    def get_coords(self, location):

        try:
            geo = self.gmaps.geocode(location)
            if not geo:
                return None

            loc = geo[0]["geometry"]["location"]
            return (loc["lat"], loc["lng"])

        except Exception:
            return None

    def run(self, dish, location):

        user_loc = self.get_coords(location)

        if not user_loc:
            return {"results": [], "ai_review": "Invalid location"}

        try:
            places = self.gmaps.places_nearby(
                location=user_loc,
                radius=5000,
                keyword=dish,
                type="restaurant"
            ).get("results", [])
        except Exception:
            return {"results": [], "ai_review": "Google Maps error"}

        results = []

        # Build restaurant list
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

        # Sort results
        results = sorted(results, key=lambda x: x["ai_score"], reverse=True)

        # Take top 3 for Gemini
        top_results = results[:3]

        # Safe Gemini prompt
        prompt = f"""
You are a food expert AI.

User searched: {dish}

Top restaurants:
{top_results}

Give:
1. Best choice
2. Why
3. One-line advice
"""

        try:
            ai_review = self.model.generate_content(prompt).text
        except Exception:
            ai_review = "AI recommendation temporarily unavailable."

        return {
            "results": results,
            "ai_review": ai_review
        }