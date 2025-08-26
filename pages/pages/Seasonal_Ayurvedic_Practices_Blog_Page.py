import streamlit as st
import pandas as pd

# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="Seasonal Ayurvedic Practices",
    page_icon="🌿",
    layout="wide"
)

# ==============================================================================
# Custom CSS for Styling
# ==============================================================================
def page_styling():
    st.markdown("""
        <style>
            .main-container {
                background-color: #f6fcf5;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            h1, h2, h3 {
                color: #106410; /* Dark Green */
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .highlight {
                color: #e74c3c;
                font-weight: bold;
            }
            .stDataFrame {
                border-radius: 8px;
                overflow: hidden;
            }
        </style>
    """, unsafe_allow_html=True)

page_styling()

# ==============================================================================
# Data for Tables
# ==============================================================================
spring_data = {
    "Foods to Favor": ["Light, dry, and warm foods", "Spices like ginger, black pepper, and turmeric", "Bitter greens", "Legumes"],
    "Foods to Avoid": ["Heavy, oily, and cold foods", "Dairy products", "Sweets", "Fried foods"]
}
summer_data = {
    "Foods to Favor": ["Cooling, hydrating, and light foods", "Fresh fruits", "Leafy greens", "Herbs like cilantro and mint"],
    "Foods to Avoid": ["Spicy, oily, and salty foods", "Fermented foods", "Red meat", "Alcohol"]
}
fall_data = {
    "Foods to Favor": ["Warm, moist, and nourishing foods", "Root vegetables", "Whole grains", "Warming spices like cinnamon and cardamom"],
    "Foods to Avoid": ["Cold, dry, and raw foods", "Caffeine", "Bitter and astringent tastes", "Light and airy foods"]
}
winter_data = {
    "Foods to Favor": ["Warm, hearty, and nourishing foods", "Soups and stews", "Whole grains", "Nuts and seeds"],
    "Foods to Avoid": ["Cold and raw foods", "Dairy products", "Sweets", "Fried foods"]
}


# ==============================================================================
# Blog Content
# ==============================================================================
with st.container(border=True):
    st.title("Seasonal Ayurvedic Practices: Staying Healthy All Year Round 🌿🕰️")
    st.markdown("---")

    st.markdown("""
    Welcome to our comprehensive guide on <span class="highlight">Seasonal Ayurvedic Practices</span>. Ayurveda, the ancient science of life, offers wisdom on how to maintain balance and health throughout the year by aligning our routines and diets with the changing seasons. Let's explore the best practices and foods for each season to help you stay vibrant and healthy all year round.
    """, unsafe_allow_html=True)

    st.header("Understanding Seasonal Routines in Ayurveda 🌞🍁❄️🌸")
    st.write("Ayurveda emphasizes living in harmony with the natural rhythms of the environment. Each season brings changes in weather and energy, which can affect our doshas (body constitutions). By adjusting our lifestyle and diet according to the season, we can maintain balance and prevent imbalances that lead to health issues.")

    # --- Spring ---
    with st.expander("### 🌸 Spring (Kapha Season)", expanded=True):
        st.write("Spring is characterized by the qualities of Kapha dosha: heavy, moist, and cool. This season can lead to an accumulation of Kapha, causing sluggishness, congestion, and allergies.")
        st.subheader("Recommended Practices")
        st.markdown("""
        - **Detoxification:** Start the season with a gentle detox to remove accumulated toxins.
        - **Exercise:** Engage in vigorous physical activities to stimulate energy and reduce Kapha.
        - **Breathing Exercises:** Practice pranayama (breathing exercises) to clear respiratory passages.
        """)
        st.subheader("Recommended Foods")
        st.dataframe(pd.DataFrame(spring_data), use_container_width=True)

    # --- Summer ---
    with st.expander("### 🌞 Summer (Pitta Season)", expanded=True):
        st.write("Summer is dominated by Pitta dosha, which brings heat, intensity, and transformation. Excess Pitta can lead to overheating, irritability, and inflammation.")
        st.subheader("Recommended Practices")
        st.markdown("""
        - **Stay Cool:** Avoid excessive heat exposure and stay hydrated.
        - **Moderate Exercise:** Engage in calming activities like swimming and yoga.
        - **Relaxation:** Incorporate cooling practices like meditation and spending time in nature.
        """)
        st.subheader("Recommended Foods")
        st.dataframe(pd.DataFrame(summer_data), use_container_width=True)

    # --- Fall ---
    with st.expander("### 🍁 Fall (Vata Season)", expanded=True):
        st.write("Fall brings the dry, cool, and windy qualities of Vata dosha. This season can lead to dryness, anxiety, and digestive issues.")
        st.subheader("Recommended Practices")
        st.markdown("""
        - **Grounding Routines:** Establish regular daily routines to provide stability.
        - **Warmth:** Keep warm and avoid exposure to cold and wind.
        - **Oil Massage:** Perform daily self-massage with warm oil to nourish and calm Vata.
        """)
        st.subheader("Recommended Foods")
        st.dataframe(pd.DataFrame(fall_data), use_container_width=True)

    # --- Winter ---
    with st.expander("### ❄️ Winter (Kapha and Vata Season)", expanded=True):
        st.write("Winter combines the cold and dry qualities of Vata with the heavy and moist qualities of Kapha. This season requires warming and nourishing practices to maintain balance.")
        st.subheader("Recommended Practices")
        st.markdown("""
        - **Stay Warm:** Dress warmly and enjoy warm beverages and foods.
        - **Exercise:** Engage in regular physical activity to counter Kapha's heaviness.
        - **Self-Care:** Include self-massage and oiling practices to nourish the body and skin.
        """)
        st.subheader("Recommended Foods")
        st.dataframe(pd.DataFrame(winter_data), use_container_width=True)

    st.header("Conclusion 🌿🕰️")
    st.markdown("""
    By aligning your lifestyle and diet with the changing seasons, you can maintain balance and support your overall health. Ayurveda offers valuable insights into how to adapt our routines and food choices to harmonize with nature's rhythms.
    """)
    st.success("Embrace these seasonal Ayurvedic practices and enjoy a healthier, more vibrant life all year round! 🌟")