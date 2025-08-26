import streamlit as st

# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="Yoga and Ayurveda Synergy",
    page_icon="🧘‍♀️",
    layout="wide"
)

# ==============================================================================
# Custom CSS for Styling
# ==============================================================================
def page_styling():
    st.markdown("""
        <style>
            .main-container {
                background-color: #f0fced;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            h1, h2 {
                color: #106410; /* Dark Green */
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .highlight {
                color: #e74c3c;
                font-weight: bold;
            }
            /* Style for the back button */
            .stButton>button {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
            }
        </style>
    """, unsafe_allow_html=True)

page_styling()

# ==============================================================================
# Blog Content
# ==============================================================================
with st.container(border=True):
    st.title("Yoga and Ayurveda: A Perfect Synergy 🧘‍♀️🌿")
    st.markdown("---")

    st.markdown("""
    Welcome to our comprehensive guide on the beautiful synergy between the <span class="highlight">Yoga</span> and <span class="highlight">Ayurveda</span>. These ancient Indian practices are more than just systems of health; they are pathways to a holistic and balanced life. Let's dive into how they connect and enhance our well-being.
    """, unsafe_allow_html=True)

    st.subheader("1. The Connection Between Yoga and Ayurveda 🔗")
    st.markdown("""
    Yoga and Ayurveda are like two sides of the same coin. They both originate from the Vedic texts and share a common goal: achieving a state of harmony in the body, mind, and spirit. Here's how they intertwine:
    - **Common Origin:** Both practices stem from the ancient Vedic culture, which provides a deep spiritual foundation.
    - **Holistic Approach:** While Ayurveda focuses on the body's health through diet, herbs, and lifestyle adjustments, Yoga emphasizes physical postures (asanas), breath control (pranayama), and meditation for mental and spiritual well-being.
    - **Balancing Doshas:** Ayurveda categorizes individuals based on three doshas (Vata, Pitta, Kapha). Yoga helps in balancing these doshas through specific asanas and practices tailored to individual needs.
    """)

    st.subheader("2. How Combining Both Practices Enhances Health and Well-Being 🌟")
    st.markdown("""
    Integrating Yoga and Ayurveda can lead to a more profound and sustainable state of health. Here’s how combining these practices benefits you:
    """)

    st.markdown("<h5>Enhanced Physical Health 🏃‍♂️</h5>", unsafe_allow_html=True)
    st.write("Yoga asanas improve flexibility, strength, and posture, while Ayurvedic principles guide you towards a diet and lifestyle that support your body type (dosha). This combination helps in preventing diseases and maintaining overall physical health.")

    st.markdown("<h5>Mental Clarity and Emotional Balance 🧘‍♀️</h5>", unsafe_allow_html=True)
    st.write("Ayurveda offers herbs and practices that nourish the mind, reducing stress and anxiety. Yoga complements this by promoting mental clarity and emotional stability through meditation and breathing exercises.")

    st.markdown("<h5>Detoxification and Rejuvenation 🌿</h5>", unsafe_allow_html=True)
    st.write("Ayurveda’s detoxifying treatments (like Panchakarma) and dietary guidelines help in cleansing the body. Yoga further aids this process through asanas that stimulate the internal organs and improve circulation, leading to a comprehensive detoxification and rejuvenation.")

    st.markdown("<h5>Spiritual Growth 🌼</h5>", unsafe_allow_html=True)
    st.write("Both Yoga and Ayurveda emphasize the connection between the individual and the universe. Practicing both can deepen your spiritual journey, fostering a sense of inner peace and purpose.")

    st.markdown("---")
    st.success("Ready to embark on this journey? 🌈 Start today and experience the transformative power of Yoga and Ayurveda!")

