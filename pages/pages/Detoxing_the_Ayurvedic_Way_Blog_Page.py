import streamlit as st

# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="Detoxing the Ayurvedic Way",
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
    st.title("Detoxing the Ayurvedic Way: Panchakarma Explained 🌿✨")
    st.markdown("---")

    st.markdown("""
    Welcome to our comprehensive guide on <span class="highlight">Detoxing the Ayurvedic Way</span>. Panchakarma, which translates to "five actions" in Sanskrit, is the ultimate Ayurvedic detoxification and rejuvenation therapy. It is a powerful process that helps to cleanse the body of accumulated toxins, balance the doshas, and restore overall health and well-being.
    """, unsafe_allow_html=True)

    st.header("Understanding Panchakarma: The Five Actions 🌟")
    st.write("Panchakarma is a personalized therapy that involves five main procedures to remove deep-rooted toxins from the body. These therapies are designed to be gentle yet profound, working to cleanse the body at a cellular level.")

    with st.expander("### 1. Vamana (Therapeutic Emesis)", expanded=False):
        st.write("Vamana is a procedure that helps to remove excess Kapha dosha from the body. It is particularly beneficial for conditions such as asthma, allergies, and skin disorders.")

    with st.expander("### 2. Virechana (Therapeutic Purgation)", expanded=False):
        st.write("Virechana is a cleansing therapy that eliminates excess Pitta dosha from the body. It is effective in treating conditions like liver disorders, skin diseases, and digestive issues.")

    with st.expander("### 3. Basti (Medicated Enema)", expanded=False):
        st.write("Basti is considered the mother of all Panchakarma treatments. It involves administering medicated oils and herbal decoctions into the colon to balance Vata dosha. It is beneficial for a wide range of conditions, including arthritis, constipation, and neurological disorders.")

    with st.expander("### 4. Nasya (Nasal Administration)", expanded=False):
        st.write("Nasya involves administering medicated oils or herbal preparations through the nasal passages. It helps to cleanse the head and neck region, improve respiratory health, and enhance mental clarity.")

    with st.expander("### 5. Raktamokshana (Bloodletting)", expanded=False):
        st.write("Raktamokshana is a traditional Ayurvedic method of blood purification. It is used to treat various skin disorders, infections, and inflammatory conditions by removing impure blood from the body.")

    st.header("Post-Panchakarma Care: Rasayana (Rejuvenation) 🌼")
    st.write("After the detoxification process, the body is receptive to rejuvenation therapies. This phase, known as Rasayana, focuses on nourishing the body, strengthening the immune system, and enhancing overall vitality.")
    st.markdown("""
    <div class="tip-item"><strong>Diet:</strong> Follow a light, nourishing diet to support digestion and assimilation. Avoid heavy, oily, and processed foods.</div>
    <div class="tip-item"><strong>Herbal Supplements:</strong> Take prescribed herbal supplements to support rejuvenation and balance.</div>
    <div class="tip-item"><strong>Lifestyle Practices:</strong> Incorporate daily routines such as yoga, meditation, and self-massage to maintain balance and well-being.</div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.success("Panchakarma is a profound Ayurvedic detoxification process that offers numerous health benefits. Consult with a qualified Ayurvedic practitioner to personalize your detox plan and achieve optimal health. 🌟")

