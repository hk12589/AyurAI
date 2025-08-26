import streamlit as st

# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="Managing Stress with Ayurveda",
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
                background-color: #f4faf3;
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
    st.title("Managing Stress with Ayurveda 🌿🧘‍♀️")
    st.markdown("---")

    st.markdown("""
    Welcome to our comprehensive guide on <span class="highlight">Managing Stress with Ayurveda</span>. In today's fast-paced world, stress has become a common issue affecting mental and physical health. Ayurveda, the ancient science of life, offers effective techniques to alleviate stress and promote mental well-being. Let's explore these techniques to help you achieve a balanced and stress-free life.
    """, unsafe_allow_html=True)

    st.header("Ayurvedic Techniques for Stress Relief 🌟")

    # --- Meditation ---
    with st.expander("### 1. Meditation 🧘‍♂️", expanded=True):
        st.write("Meditation is a powerful Ayurvedic practice that calms the mind, reduces stress, and enhances mental clarity. Regular meditation helps in balancing the doshas and promotes inner peace.")
        st.markdown("""
        - **Mindfulness Meditation:** Focus on your breath and observe your thoughts without judgment. This practice helps in grounding and calming the mind.
        - **Guided Meditation:** Listen to guided meditation recordings to relax and de-stress. These often include calming music and instructions.
        - **Mantra Meditation:** Repeating a soothing mantra, such as "Om," can help in centering your mind and reducing stress.
        """)

    # --- Yoga ---
    with st.expander("### 2. Yoga 🧘‍♀️", expanded=True):
        st.write("Yoga is a holistic practice that combines physical postures, breathing exercises, and meditation. It helps in releasing physical tension, improving flexibility, and calming the mind.")
        st.markdown("""
        - **Asanas (Postures):** Practice gentle yoga postures like Child's Pose (Balasana), Cat-Cow Pose (Marjaryasana-Bitilasana), and Corpse Pose (Savasana) to relieve stress.
        - **Pranayama (Breathing Exercises):** Techniques like Nadi Shodhana (Alternate Nostril Breathing) are effective in calming the nervous system.
        - **Relaxation Techniques:** Incorporate yoga nidra (yogic sleep) to deeply relax your body and mind.
        """)

    # --- Herbal Remedies ---
    with st.expander("### 3. Herbal Remedies 🌿", expanded=True):
        st.write("Ayurveda offers a variety of herbal remedies that help in managing stress. These herbs have adaptogenic properties that support the body's ability to cope with stress.")
        st.markdown("""
        - **Ashwagandha:** Known for its adaptogenic properties, Ashwagandha helps in reducing stress, anxiety, and fatigue.
        - **Brahmi:** A brain tonic that enhances cognitive function, reduces anxiety, and promotes mental clarity.
        - **Jatamansi:** Effective in calming the mind, reducing stress, and improving sleep quality.
        - **Shankhapushpi:** Known for its calming effects on the nervous system and helps in reducing mental stress and anxiety.
        """)

    st.header("Additional Ayurvedic Tips for Stress Management 🌸")
    
    st.markdown("""
    <div class="tip-item"><strong>Daily Routine:</strong> Establish a consistent daily routine to create stability and reduce stress. Wake up early, eat at regular times, and go to bed early.</div>
    <div class="tip-item"><strong>Diet:</strong> Eat a balanced diet that supports your dosha. Include fresh, organic, and whole foods. Avoid processed foods, caffeine, and excessive sugar.</div>
    <div class="tip-item"><strong>Self-Massage:</strong> Practice Abhyanga (self-massage) with warm sesame oil to calm the nervous system and promote relaxation.</div>
    <div class="tip-item"><strong>Aromatherapy:</strong> Use essential oils like lavender, sandalwood, and chamomile in diffusers or during massage to reduce stress.</div>
    <div class="tip-item"><strong>Hydration:</strong> Stay hydrated by drinking warm water or herbal teas throughout the day.</div>
    <div class="tip-item"><strong>Sleep:</strong> Ensure you get adequate sleep by maintaining a regular sleep schedule and creating a calming bedtime routine.</div>
    """, unsafe_allow_html=True)


    st.markdown("---")
    st.success("By incorporating these Ayurvedic techniques into your daily routine, you can effectively manage stress and enhance your mental well-being. �")