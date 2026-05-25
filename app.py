import streamlit as st
from agent import TasteTrailAgent

st.set_page_config(page_title="Taste Trail AI 🍔", layout="centered")

st.title("🍔 Taste Trail AI")
st.write("AI-powered food discovery using Google Maps + Gemini")

dish = st.text_input("Enter dish (e.g., burger, pizza)")
location = st.text_input("Enter location (e.g., Toronto)")

if st.button("Find Best Food"):

    agent = TasteTrailAgent()
    data = agent.run(dish, location)

    results = data["results"]

    if not results:
        st.warning(data["ai_review"])
    else:

        st.success(f"Found {len(results)} restaurants")

        # AI Insight Box
        st.markdown("## 🤖 AI Recommendation")
        st.info(data["ai_review"])

        st.markdown("---")

        # Restaurant Cards
        for r in results:

            st.markdown(f"### 🍽️ {r['name']}")
            st.write(f"⭐ Rating: {r['rating']}")
            st.write(f"📍 Distance: {r['distance_km']} km")
            st.write(f"🧠 AI Score: {r['ai_score']}")
            st.markdown("---")