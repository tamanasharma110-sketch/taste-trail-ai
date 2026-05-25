import streamlit as st
from agent import TasteTrailAgent

st.set_page_config(page_title="Taste Trail AI 🍔", layout="centered")

st.title("🍔 Taste Trail AI")
st.write("Find real restaurants + real user reviews near you")

dish = st.text_input("Enter dish (e.g., pizza, burger, biryani)")
location = st.text_input("Enter location (e.g., Toronto)")

if st.button("Find Best Places"):

    agent = TasteTrailAgent()
    results = agent.run(dish, location)

    if not results:
        st.error("No results found or API error")
    else:

        st.success(f"Found {len(results)} restaurants")

        for r in results:

            st.markdown(f"## 🍽️ {r['name']}")
            st.write(f"⭐ Rating: {r['rating']}")
            st.write(f"📍 Distance: {r['distance_km']} km")
            st.write(f"🧠 Score: {r['score']}")

            st.markdown("### 🧑 Real User Reviews")

            if r["reviews"]:
                for rev in r["reviews"]:
                    st.markdown(f"- **{rev['author']}**: {rev['text']}")
            else:
                st.write("No reviews available")

            st.markdown("---")