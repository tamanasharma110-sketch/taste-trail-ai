import streamlit as st
from agent import TasteTrailAgent

st.set_page_config(page_title="Taste Trail AI 🍔", layout="centered")

st.title("🍔 Taste Trail AI")
st.write("AI-powered restaurant discovery with real-time ranking + Gemini insights")

dish = st.text_input("Enter dish (e.g., burger, pizza, biryani)")
location = st.text_input("Enter your location")

if st.button("Find Best Places"):

    if not dish or not location:
        st.warning("Please enter both fields")
    else:
        agent = TasteTrailAgent()
        data = agent.run(dish, location)

        if not data:
            st.error("No results found")
        else:
            results = data["results"]

            st.success(f"Found {len(results)} restaurants")

            # 🌟 Gemini AI Insight Box
            st.markdown("## 🤖 AI Recommendation")
            st.info(data["ai_review"])

            st.markdown("---")

            # 🍽️ Restaurant Cards
            for r in results:

                st.markdown("### 🍽️ " + r["name"])

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write(f"⭐ {r['rating']}")

                with col2:
                    st.write(f"📍 {r['distance_km']} km")

                with col3:
                    st.write(f"🧠 Score: {r['ai_score']}")

                st.markdown("---")