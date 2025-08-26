import streamlit as st

# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="Top 10 Ayurvedic Herbs",
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
                background-color: #f8fff7;
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
            strong {
                font-weight: 600;
            }
        </style>
    """, unsafe_allow_html=True)

page_styling()

# ==============================================================================
# Blog Content
# ==============================================================================
with st.container(border=True):
    st.title("Top 10 Ayurvedic Herbs for Daily Health 🌿✨")
    st.markdown("---")

    st.markdown("""
    Welcome to our guide on the <span class="highlight">Top 10 Ayurvedic Herbs</span> for daily health. These herbs have been used for centuries in Ayurveda to promote health, prevent diseases, and enhance overall well-being. Let's explore their benefits and how to incorporate them into your daily routine.
    """, unsafe_allow_html=True)

    # --- Herb 1: Ashwagandha ---
    st.header("1. Ashwagandha 🌱")
    st.markdown("**Benefits:** Ashwagandha is known for its adaptogenic properties, helping the body manage stress. It boosts energy levels, supports the immune system, and enhances cognitive function.")
    st.markdown("**How to Use:** Take 1-2 teaspoons of Ashwagandha powder mixed with warm milk or water before bed. You can also find it in capsule form.")

    # --- Herb 2: Turmeric ---
    st.header("2. Turmeric �")
    st.markdown("**Benefits:** Turmeric has powerful anti-inflammatory and antioxidant properties. It supports joint health, boosts immunity, and aids in digestion.")
    st.markdown("**How to Use:** Add a teaspoon of turmeric powder to your daily cooking, smoothies, or warm milk. Golden milk, made with turmeric and milk, is a popular drink.")

    # --- Herb 3: Triphala ---
    st.header("3. Triphala 🌿")
    st.markdown("**Benefits:** Triphala, a blend of three fruits (Amla, Haritaki, and Bibhitaki), supports digestive health, detoxifies the body, and improves skin health.")
    st.markdown("**How to Use:** Take 1 teaspoon of Triphala powder with warm water before bed or in the morning on an empty stomach.")

    # --- Herb 4: Brahmi ---
    st.header("4. Brahmi 🌾")
    st.markdown("**Benefits:** Brahmi is known for enhancing memory, concentration, and cognitive function. It also helps reduce anxiety and stress.")
    st.markdown("**How to Use:** Take Brahmi powder with warm water or milk. It is also available in capsule form.")

    # --- Herb 5: Tulsi (Holy Basil) ---
    st.header("5. Tulsi (Holy Basil) 🌿")
    st.markdown("**Benefits:** Tulsi is revered for its immune-boosting properties. It also helps in relieving respiratory conditions, reducing stress, and promoting longevity.")
    st.markdown("**How to Use:** Brew Tulsi leaves as a tea or add Tulsi powder to your daily smoothie.")

    # --- Herb 6: Shatavari ---
    st.header("6. Shatavari 🌸")
    st.markdown("**Benefits:** Shatavari is particularly beneficial for women’s health. It supports reproductive health, balances hormones, and enhances vitality.")
    st.markdown("**How to Use:** Mix Shatavari powder with warm milk or water. It can also be taken in capsule form.")

    # --- Herb 7: Neem ---
    st.header("7. Neem 🍃")
    st.markdown("**Benefits:** Neem has strong antibacterial and antifungal properties. It supports skin health, detoxifies the blood, and boosts immunity.")
    st.markdown("**How to Use:** Neem powder can be taken with water or applied topically as a paste for skin issues.")

    # --- Herb 8: Licorice Root ---
    st.header("8. Licorice Root 🍭")
    st.markdown("**Benefits:** Licorice root supports digestive health, soothes inflammation, and enhances respiratory health.")
    st.markdown("**How to Use:** Brew licorice root as a tea or take it in powdered form with warm water.")

    # --- Herb 9: Amla (Indian Gooseberry) ---
    st.header("9. Amla (Indian Gooseberry) 🍏")
    st.markdown("**Benefits:** Amla is rich in Vitamin C and antioxidants. It supports immune health, enhances digestion, and promotes healthy hair and skin.")
    st.markdown("**How to Use:** Consume Amla juice daily or take Amla powder with honey or warm water.")

    # --- Herb 10: Guggul ---
    st.header("10. Guggul 🧪")
    st.markdown("**Benefits:** Guggul helps in detoxifying the body, supports weight management, and promotes healthy cholesterol levels.")
    st.markdown("**How to Use:** Take Guggul resin or powder as directed by an Ayurvedic practitioner, often in tablet or capsule form.")

    st.markdown("---")
    st.success("Embrace the power of Ayurveda and experience the transformative benefits of these ancient herbs in your life! 🌟")