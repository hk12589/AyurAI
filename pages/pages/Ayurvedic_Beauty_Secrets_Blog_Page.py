import streamlit as st

# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="Ayurvedic Beauty Secrets",
    page_icon="✨",
    layout="wide"
)

# ==============================================================================
# Custom CSS for Styling
# ==============================================================================
def page_styling():
    st.markdown("""
        <style>
            .main-container {
                background-color: #f7fff5;
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
            .tip-item {
                background-color: #ecf0f1;
                margin: 10px 0;
                padding: 15px;
                border-radius: 5px;
                border-left: 5px solid #16a085;
            }
        </style>
    """, unsafe_allow_html=True)

page_styling()

# ==============================================================================
# Blog Content
# ==============================================================================
with st.container(border=True):
    st.title("Ayurvedic Beauty Secrets: Natural Ways to Glow 🌿✨")
    st.markdown("---")

    st.markdown("""
    Welcome to our comprehensive guide on <span class="highlight">Ayurvedic Beauty Secrets</span>. Ayurveda offers a treasure trove of natural remedies for achieving radiant skin and healthy hair. Let's dive into the secrets to a natural glow.
    """, unsafe_allow_html=True)

    st.header("Ayurvedic Tips for Healthy Skin 🌟")

    with st.expander("### 1. Abhyanga (Self-Massage) �", expanded=True):
        st.write("Abhyanga is a daily self-massage practice using warm oil. It nourishes the skin, improves blood circulation, and promotes detoxification.")
        st.markdown("""
        - **Vata Dosha:** Use warm sesame or almond oil.
        - **Pitta Dosha:** Use cooling oils like coconut or sunflower oil.
        - **Kapha Dosha:** Use warming oils like mustard or sesame oil.
        """)

    with st.expander("### 2. Ubtan (Herbal Scrub) 🌿", expanded=True):
        st.write("Ubtan is a traditional Ayurvedic herbal scrub used to exfoliate and cleanse the skin, removing dead skin cells and improving complexion.")
        st.markdown("""
        - **Ingredients:** Mix chickpea flour, turmeric, sandalwood powder, and rose water to form a paste.
        - **Application:** Apply the paste to your face and body, gently scrub in circular motions, and rinse with lukewarm water.
        """)

    with st.expander("### 3. Natural Face Masks 🌸", expanded=True):
        st.write("Ayurveda recommends using natural ingredients for face masks to nourish and rejuvenate the skin.")
        st.markdown("""
        - **For Glowing Skin:** Mix 1 tbsp honey, 1 tbsp yogurt, and a pinch of turmeric. Apply, leave for 15 minutes, and rinse.
        - **For Acne-Prone Skin:** Mix 1 tbsp neem powder, 1 tbsp aloe vera gel, and a few drops of tea tree oil. Apply, leave for 15 minutes, and rinse.
        - **For Dry Skin:** Mix 1 mashed avocado, 1 tbsp honey, and a few drops of olive oil. Apply, leave for 15 minutes, and rinse.
        """)

    st.header("Ayurvedic Tips for Healthy Hair 🌿")

    with st.expander("### 1. Scalp Massage 🌿", expanded=True):
        st.write("Regular scalp massages with Ayurvedic oils can strengthen hair roots and promote hair growth.")
        st.markdown("""
        - **Vata Dosha:** Use warm bhringraj oil or sesame oil.
        - **Pitta Dosha:** Use cooling oils like amla oil or coconut oil.
        - **Kapha Dosha:** Use stimulating oils like rosemary oil mixed with a base oil.
        """)

    with st.expander("### 2. Herbal Hair Masks 🌿", expanded=True):
        st.write("Ayurvedic herbal hair masks nourish the scalp, condition the hair, and prevent hair fall.")
        st.markdown("""
        - **For Hair Growth:** Mix 2 tbsp amla powder, 1 tbsp bhringraj powder, and water to form a paste. Apply to scalp and hair, leave for 30 minutes, and rinse.
        - **For Dandruff:** Mix 2 tbsp neem powder, 1 tbsp yogurt, and a few drops of tea tree oil. Apply to scalp, leave for 30 minutes, and rinse.
        - **For Conditioning:** Mix 1 mashed banana, 1 tbsp honey, and a few drops of almond oil. Apply to hair, leave for 30 minutes, and rinse.
        """)

    st.header("Diet and Lifestyle for Natural Beauty 🌿")
    st.write("Healthy skin and hair start from within. Follow these Ayurvedic tips:")
    st.markdown("""
    <div class="tip-item"><strong>Hydration:</strong> Drink plenty of water and herbal teas to keep your skin and hair hydrated.</div>
    <div class="tip-item"><strong>Balanced Diet:</strong> Eat a diet rich in fresh fruits, vegetables, whole grains, and healthy fats. Avoid processed foods, excessive sugar, and caffeine.</div>
    <div class="tip-item"><strong>Stress Management:</strong> Practice yoga, meditation, and deep breathing exercises to manage stress.</div>
    <div class="tip-item"><strong>Sleep:</strong> Ensure you get adequate sleep to allow your body to repair and rejuvenate.</div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.success("By incorporating Ayurvedic beauty secrets into your daily routine, you can achieve radiant skin and healthy hair naturally. Let your inner beauty glow! 🌟")