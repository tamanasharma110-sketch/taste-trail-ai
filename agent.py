import googlemaps
from geopy.distance import geodesic


class TasteTrailAgent:

    def __init__(self):
        self.gmaps = googlemaps.Client(key="AIzaSyCtA_07Sq9GkxNCd8ZsGVgSPPKcFVJyFqg")

    # --------------------------
    # Convert location text → lat/lng
    # --------------------------
    def get_coords(self, location_text):

        geo = self.gmaps.geocode(location_text)

        if not geo:git --version
            return None

        loc = geo[0]["geometry"]["location"]

        return (loc["lat"], loc["lng"])

    # --------------------------
    # Get nearby restaurants
    # --------------------------
    def get_places(self, dish, user_loc):

        places = self.gmaps.places_nearby(
            location=user_loc,
            radius=5000,
            keyword=dish,
            type="restaurant"
        )

        return places.get("results", [])

    # --------------------------
    # Get reviews (with people id)
    # --------------------------
    def get_reviews(self, place_id):

        try:
            details = self.gmaps.place(
                place_id=place_id,
                fields=["reviews"]
            )

            reviews = details.get("result", {}).get("reviews", [])

            output = []

            for r in reviews[:3]:  # top 3 reviews only

                output.append({
                    "person_id": r.get("author_name", "Anonymous"),
                    "text": r.get("text", "Good food and service"),
                    "rating": r.get("rating", 0)
                })

            return output

        except:
            return []

    # --------------------------
    # AI recommendation logic
    # --------------------------
    def ai_recommendation(self, name, rating, distance):

        if rating >= 4.5:
            return f"{name} is highly recommended due to excellent customer satisfaction and top-rated food quality."

        if distance < 2:
            return f"{name} is very close to your location, making it a convenient choice."

        if rating >= 4.0:
            return f"{name} is a solid choice with good reviews and decent service."

        return f"{name} is an average option, but still worth trying if nearby."

    # --------------------------
    # MAIN FUNCTION
    # --------------------------
    def run(self, query, location_text):

        user_loc = self.get_coords(location_text)

        if not user_loc:
            return []

        places = self.get_places(query, user_loc)

        results = []

        for p in places:

            name = p.get("name")
            rating = p.get("rating", 0)

            loc = p["geometry"]["location"]
            place_id = p.get("place_id")

            distance = geodesic(
                user_loc,
                (loc["lat"], loc["lng"])
            ).km

            reviews = self.get_reviews(place_id)

            ai_text = self.ai_recommendation(name, rating, distance)

            results.append({
                "restaurant": name,
                "rating": round(rating, 2),
                "distance_km": round(distance, 2),
                "reviews": reviews,
                "ai_recommendation": ai_text
            })

        return sorted(results, key=lambda x: x["rating"], reverse=True)