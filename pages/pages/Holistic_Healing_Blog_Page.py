import streamlit as st

# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="Holistic Healing: Combining Ayurveda & Modern Medicine",
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
            .case-study {
                background-color: #ecf0f1;
                padding: 1.5rem;
                border-radius: 10px;
                margin-top: 1rem;
                border-left: 5px solid #16a085;
            }
        </style>
    """, unsafe_allow_html=True)

page_styling()

# ==============================================================================
# Blog Content
# ==============================================================================
with st.container(border=True):
    st.title("Holistic Healing: Combining Ayurveda with Modern Medicine 🌿🔬")
    st.markdown("---")

    st.markdown("""
    Welcome to our blog on <span class="highlight">Holistic Healing</span>, where we explore the benefits of integrating Ayurvedic practices with modern medical treatments. Combining these two approaches can offer a comprehensive and balanced pathway to health and wellness. Let's dive into the advantages and explore some success stories.
    """, unsafe_allow_html=True)

    st.header("Benefits of Integrating Ayurvedic Practices 🌟")

    st.subheader("1. Complementary Strengths �")
    st.write("Ayurveda and modern medicine have unique strengths that complement each other. Ayurveda focuses on prevention, holistic wellness, and natural remedies, while modern medicine excels in acute care, diagnostics, and surgical interventions. Together, they provide a more complete approach to health.")

    st.subheader("2. Personalized Treatment Plans 🧩")
    st.write("Ayurveda offers personalized treatment based on an individual's dosha (body constitution) and imbalances, while modern medicine uses diagnostic tools and tests to tailor treatments. Combining both can create a more precise and effective treatment plan.")

    st.subheader("3. Enhanced Disease Management ⚖️")
    st.write("Integrating Ayurvedic practices can enhance the management of chronic diseases. For example, incorporating Ayurvedic herbs and dietary changes can support conventional treatments for diabetes, hypertension, and arthritis, leading to improved outcomes and reduced side effects.")

    st.subheader("4. Stress Reduction and Mental Health 🧘‍♀️")
    st.write("Ayurvedic practices like meditation, yoga, and herbal remedies are effective in reducing stress and anxiety. When combined with modern psychological therapies and medications, patients can achieve better mental health and emotional balance.")

    st.subheader("5. Holistic Recovery and Rehabilitation 🌼")
    st.write("Post-surgery or during recovery from illnesses, Ayurvedic therapies such as Panchakarma (detoxification) and Rasayana (rejuvenation) can aid in faster and more holistic recovery, enhancing overall well-being and vitality.")

    st.header("Case Studies and Success Stories 📖")

    with st.container():
        st.markdown('<div class="case-study">', unsafe_allow_html=True)
        st.subheader("Case Study 1: Managing Diabetes")
        st.write("""
        John, a 55-year-old man, was diagnosed with Type 2 diabetes. His treatment plan included conventional medications to manage blood sugar levels. Additionally, he consulted an Ayurvedic practitioner who recommended dietary changes, including incorporating bitter gourd and fenugreek, as well as practicing yoga daily.
        
        Over six months, John experienced improved blood sugar control, weight loss, and increased energy levels. The integration of Ayurvedic diet and lifestyle changes with his medication regimen helped him achieve a more balanced and sustainable health outcome.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="case-study">', unsafe_allow_html=True)
        st.subheader("Case Study 2: Combating Stress and Anxiety")
        st.write("""
        Susan, a 30-year-old marketing executive, struggled with chronic stress and anxiety. She received cognitive behavioral therapy (CBT) and medication from her psychiatrist, which provided some relief. However, she still felt overwhelmed.
        
        She decided to incorporate Ayurvedic practices into her routine, including daily meditation, Ashwagandha supplements, and a Vata-balancing diet. Within a few months, Susan noticed a significant reduction in anxiety levels, better sleep, and an overall sense of calm.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="case-study">', unsafe_allow_html=True)
        st.subheader("Case Study 3: Post-Surgical Recovery")
        st.write("""
        Mary, a 45-year-old woman, underwent surgery for a knee replacement. Her post-surgical care included physical therapy and pain management medication. To support her recovery, Mary also engaged in Ayurvedic therapies such as Abhyanga (oil massage) and followed a Kapha-pacifying diet.
        
        Her holistic approach led to a faster recovery, reduced inflammation, and improved mobility.
        """)
        st.markdown('</div>', unsafe_allow_html=True)


    st.header("Conclusion 🌿🔬")
    st.markdown("""
    Combining Ayurveda with modern medicine provides a powerful, holistic approach to health and wellness. By leveraging the strengths of both systems, patients can achieve better health outcomes, manage chronic conditions more effectively, and enjoy a higher quality of life.
    """)
    st.success("Are you ready to embrace holistic healing? Explore the benefits of integrating Ayurvedic practices with your medical treatments! 🌟")