import streamlit as st
from agent import TasteTrailAgent

st.title("🍔 AI Food Recommendation System")

agent = TasteTrailAgent()

dish = st.text_input("Enter dish (burger, pizza, etc.)")
location = st.text_input("Enter your location (Brampton, Toronto, etc.)")

if st.button("Find Restaurants"):

    results = agent.run(dish, location)

    if not results:
        st.error("No restaurants found")

    else:

        st.success(f"Found {len(results)} restaurants")

        for r in results:

            st.markdown("---")
            st.subheader(r["restaurant"])

            st.write("⭐ Rating:", r["rating"])
            st.write("📍 Distance:", r["distance_km"], "km")

            st.write("📝 Top Reviews:")

            for rev in r["reviews"]:
                st.write(f"👤 {rev['person_id']} (⭐{rev['rating']}): {rev['text']}")

            st.success("🧠 AI Recommendation")
            st.write(r["ai_recommendation"])