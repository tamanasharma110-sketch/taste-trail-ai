import streamlit as st
from agent import TasteTrailAgent

st.set_page_config(page_title="Taste Trail AI 🍔", layout="centered")

st.title("🍔 Taste Trail AI")
st.write("Find best nearby restaurants using AI ranking + distance")

dish = st.text_input("Enter dish (e.g., burger, pizza, biryani)")
location = st.text_input("Enter your location (e.g., Toronto)")

if st.button("Search"):

    if not dish or not location:
        st.warning("Please enter both dish and location")
    else:
        agent = TasteTrailAgent()
        results = agent.run(dish, location)

        if not results:
            st.error("No results found")
        else:
            st.success(f"Found {len(results)} restaurants")

            for r in results:

                st.markdown("---")
                st.subheader(r["name"])

                st.write(f"⭐ Rating: {r['rating']}")
                st.write(f"📍 Distance: {r['distance_km']} km")
                st.write(f"🧠 AI Score: {r['ai_score']}")