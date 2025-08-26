import streamlit as st
import pandas as pd

# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="Ayurvedic Diet: According to Your Dosha",
    page_icon="🍽️",
    layout="wide"
)

# ==============================================================================
# Custom CSS for Styling
# ==============================================================================
def page_styling():
    st.markdown("""
        <style>
            .main-container {
                background-color: #f9fff8;
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
vata_data = {
    "Foods to Favor": ["Warm, cooked foods", "Soups & Stews", "Root vegetables", "Nuts and seeds", "Dairy", "Sweet, sour, and salty tastes"],
    "Foods to Avoid": ["Cold and raw foods", "Caffeine", "Bitter and astringent tastes", "Dry foods", "Light and airy foods", "---"] # Using --- as a filler
}
pitta_data = {
    "Foods to Favor": ["Cooling foods", "Fresh fruits and vegetables", "Dairy", "Sweet, bitter, and astringent tastes", "Whole grains", "Legumes"],
    "Foods to Avoid": ["Spicy and fried foods", "Sour and salty tastes", "Alcohol", "Red meat", "Caffeine", "Excessive oil"]
}
kapha_data = {
    "Foods to Favor": ["Light and warm foods", "Spices", "Fruits and vegetables", "Legumes", "Bitter, pungent, and astringent tastes", "---"],
    "Foods to Avoid": ["Heavy and oily foods", "Dairy", "Sweet, sour, and salty tastes", "Processed foods", "Cold and raw foods", "---"]
}

# ==============================================================================
# Blog Content
# ==============================================================================
with st.container(border=True):
    st.title("Ayurvedic Diet: Eating According to Your Dosha 🍽️🌿")
    st.markdown("---")

    st.markdown("""
    Welcome to our guide on the <span class="highlight">Ayurvedic Diet</span>, where we explore how eating according to your dosha can enhance your health and well-being. Ayurveda, the ancient Indian system of medicine, emphasizes the importance of a balanced diet tailored to your individual constitution. Let's dive into the world of doshas and discover the best dietary practices for each type.
    """, unsafe_allow_html=True)

    st.header("Understanding Doshas 🌀")
    st.markdown("""
    In Ayurveda, doshas are the fundamental energies that govern our physical and mental processes. There are three primary doshas:
    - **Vata** (Air and Ether): Governs movement, circulation, and communication.
    - **Pitta** (Fire and Water): Controls digestion, metabolism, and energy production.
    - **Kapha** (Earth and Water): Provides structure, lubrication, and stability.
    
    Each person has a unique combination of these doshas, which influences their physical and mental characteristics. Imbalances in doshas can lead to health issues, and diet is a key factor in maintaining balance.
    """)

    st.header("Dietary Recommendations for Each Dosha 🥗")

    # --- Vata Dosha ---
    with st.expander("🍃 Vata Dosha Diet", expanded=True):
        st.write("Vata individuals are typically energetic, creative, and lively. When out of balance, they may experience anxiety, dry skin, and digestive issues.")
        st.dataframe(pd.DataFrame(vata_data), use_container_width=True)

    # --- Pitta Dosha ---
    with st.expander("🔥 Pitta Dosha Diet", expanded=True):
        st.write("Pitta individuals are usually passionate, intelligent, and strong-willed. When out of balance, they can experience anger, inflammation, and digestive problems.")
        st.dataframe(pd.DataFrame(pitta_data), use_container_width=True)

    # --- Kapha Dosha ---
    with st.expander("🌍 Kapha Dosha Diet", expanded=True):
        st.write("Kapha individuals are generally calm, steady, and nurturing. When out of balance, they may face weight gain, lethargy, and congestion.")
        st.dataframe(pd.DataFrame(kapha_data), use_container_width=True)


    st.header("Incorporating Ayurvedic Dietary Practices into Your Daily Routine 🌱")
    st.markdown("""
    Here are some tips to help you incorporate Ayurvedic dietary practices into your daily life:
    - **Eat Mindfully:** Pay attention to your food, chew slowly, and enjoy the flavors.
    - **Follow a Routine:** Eat at regular times each day to support your digestive health.
    - **Balance Tastes:** Ensure your meals include all six tastes: sweet, sour, salty, bitter, pungent, and astringent, with an emphasis on the tastes that balance your dosha.
    - **Stay Hydrated:** Drink warm water or herbal teas throughout the day.
    - **Seasonal Eating:** Adjust your diet according to the seasons, as each season affects the doshas differently.
    """)

    st.markdown("---")
    st.success("Ready to start your Ayurvedic dietary journey? Embrace these practices and experience the transformative power of eating according to your dosha! 🌿")
