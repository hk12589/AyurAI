import streamlit as st
import textwrap

with st.sidebar:    
    "[AI Doctor](app.py)"
    "[Prakriti Finder](Pages/prakriti.py)"

# ==============================================================================
# DATA DEFINITIONS
# This data is sourced directly from the original JS files.
# ==============================================================================

QUIZ_DATA = [
    {
        "Q": "How is your body structure?",
        "C": ["Thin & lean", "Medium & proportionate", "Large & well-built"],
    },
    {
        "Q": "How is your appetite?",
        "C": [
            "Irregular: I feel hungry sometimes and other times I do not",
            "Regular: I feel hunger strongly every few hours and need food at regular intervals",
            "Steady: I do not feel hungry for a few hours, I can miss meals, but do not like to. I tend towards emotional eating.",
        ],
    },
    {
        "Q": "What is your hair texture like?",
        "C": [
            "Thin, tends to be dry, split ends",
            "Medium thickness, tends to thin out, more hair fall",
            "Thick, luscious, tends to be more greasy than dry",
        ],
    },
    {
        "Q": "How is your skin?",
        "C": [
            "Dry, thin, & rough",
            "Sensitive - oily/sometimes I am prone to acne, inflammation, pimples, sweat more",
            "Oily/combination - I rarely use moisturizer/do not feel like it. My skin tends to be well-hydrated, smooth and soft - moist/greasy",
        ],
    },
    {
        "Q": "My lifelong weight tendency has been",
        "C": [
            "I am thin and find it difficult to gain weight",
            "Steady, medium, consistent and it reflects my efforts - easy to put on, easy to lose",
            "Slightly overweight - I have a stocky build and can gain weight easily - difficulty to lose weight",
        ],
    },
    {
        "Q": "How do you respond to climate?",
        "C": [
            "I tend to feel extremely cold easily",
            "I cannot stand extreme heat and tend to overheat easily",
            "Neutral, but I prefer warm climates - aversion to moist rainy and cool weather",
        ],
    },
    {
        "Q": "How do you sleep?",
        "C": [
            "I sleep fewer hours than normal, and my sleep tends to get disturbed. I am a light sleeper - interrupted",
            "Moderately. I usually sleep between 6-8 hours",
            "I can easily sleep for over 8 hours. My sleep tends to be heavy, long and deeply restful - sleepy & lazy",
        ],
    },
    {
        "Q": "How is your stamina?",
        "C": [
            "Delicate - I feel exhausted easily in the evenings, after not doing much work",
            "Moderate, but I have a strong will and can do anything I set my mind to",
            "Incredible, but I am sometimes hesitant to push myself and test it. Excellent energy",
        ],
    },
    {
        "Q": "Mentally, I tend to be",
        "C": [
            "Flexible, creative, restless, quick",
            "Strong, determined, competitive, ambitious, smart, intellect aggressive",
            "Calm, stable, steady, loving, reliable",
        ],
    },
    {
        "Q": "How are you as a learner?",
        "C": [
            "I learn quickly, but also forget quickly",
            "I am sharp and learn whatever I set my mind to",
            "It takes me time to learn something but once I do I never forget it",
        ],
    },
    {
        "Q": "I am...",
        "C": [
            "Creative, free-willed, excited, quick, restless",
            "Ambitious, driven, analytical",
            "Warm, loving, kind, calm, stable",
        ],
    },
    {
        "Q": "What feelings are you most prone to?",
        "C": [
            "Feeling anxious, nervous, fear, worry",
            "Impatience, irritability, frustration, aggression",
            "Lethargy, lack of motivation, slightly depressed, slow moving, calm reclusive",
        ],
    },
    {
        "Q": "What are you prone to?",
        "C": [
            "Pain in my joints, cracking joints",
            "Acidity, Acid reflux",
            "Prone to mucus formation in the nose, sinus, nose to chest related issues",
        ],
    },
    {
        "Q": "How are your stools?",
        "C": [
            "Dry and hard scanty, tend to constipation",
            "Soft, loose stools",
            "Heavy, thick, Sticky, oily, regular",
        ],
    },
    {
        "Q": "How is your digestion",
        "C": [
            "Delicate - I cannot tolerate all foods, sometimes its great and other times it acts up",
            "Strong - I can tolerate most foods and my metabolism is fast",
            "Slow - I feel tired after meals",
        ],
    },
    {
        "Q": "What is your personality?",
        "C": [
            "Idealistic, creative, free-flowing",
            "Goal-oriented, competitive, ambitious",
            "Calm, peaceful, slow, loyal",
        ],
    },
    {
        "Q": "How do you tend to be in difficulty?",
        "C": [
            "Nervous, anxious, worried & irritable",
            "Impatient & aggressive",
            "I am sometimes depressive, tend to avoid my emotions and avoid uncomfortable situations",
        ],
    },
    {
        "Q": "Hunger",
        "C": [
            "Irregular, anytime",
            "Sudden hunger pangs, sharp hunger",
            "Can skip any meal easily",
        ],
    },
    {
        "Q": "Mood",
        "C": [
            "Changes quickly and has frequent mood swings",
            "Eats at moderate speed",
            "Stable",
        ],
    },
]

RESULT_DATA = {
    "Vata Dosha": {
        "Lifestyle":
            "Establish a regular daily routine, prioritize calm and consistency",
        "Diet": "Emphasize warm, grounding foods like cooked grains, root vegetables, and warm spices. Avoid excessive cold or raw foods.",
        "Wellness":
            "Practice gentle and calming exercises like yoga or tai chi. Adequate rest and sleep are crucial.",
    },
    "Pitta Dosha": {
        "Lifestyle":
            "Create a balanced routine with time for relaxation. Avoid excessive competition or stress.",
        "Diet": "Choose cooling and hydrating foods like cucumber, mint, and coconut. Minimize spicy and acidic foods.",
        "Wellness":
            "Engage in moderate, non-competitive physical activities. Meditation and mindfulness can help manage stress.",
    },
    "Kapha Dosha": {
        "Lifestyle":
            "Encourage active and energetic habits, avoid excessive sedentary behavior.",
        "Diet": "Favor warm, light, and spicy foods. Limit heavy and oily foods. Include a variety of colorful fruits and vegetables.",
        "Wellness":
            "Regular, invigorating exercise is crucial. Stimulate the mind with new experiences. Incorporate dry brushing to invigorate circulation.",
    },
}

# ==============================================================================
# STREAMLIT APP LOGIC
# ==============================================================================

# --- Function to initialize or reset the quiz state ---
def initialize_state():
    """Initializes the session state for the quiz."""
    st.session_state.current_question_index = 0
    st.session_state.vata = 0
    st.session_state.pitta = 0
    st.session_state.kapha = 0
    st.session_state.show_result = False
    st.session_state.prakriti_result = ""
    st.session_state.selected_option = None


# --- Function to determine Prakriti ---
def determine_prakriti():
    """Calculates the final Prakriti using the exact logic from Quiz.js."""
    vata = st.session_state.vata
    pitta = st.session_state.pitta
    kapha = st.session_state.kapha

    if vata > pitta and vata > kapha:
        return "Vata"
    elif pitta > vata and pitta > kapha:
        return "Pitta"
    elif kapha > pitta and kapha > vata:
        return "Kapha"
    else:
        if vata < pitta and pitta == kapha:
            return "Pitta and Kapha"
        elif kapha < pitta and vata == pitta:
            return "Vata and Pitta"
        elif pitta < vata and vata == kapha:
            return "Vata and Kapha"
        else:
            return "Vata and Pitta and Kapha"

# --- Function to display the quiz questions and options ---
def display_quiz():
    """Displays the current question and handles user interaction."""
    st.subheader(f"Question {st.session_state.current_question_index + 1}/{len(QUIZ_DATA)}")
    
    question_data = QUIZ_DATA[st.session_state.current_question_index]
    st.markdown(f"### {question_data['Q']}")
    
    # Use st.radio for the options. The key is crucial for Streamlit to track the widget's state.
    selected_option = st.radio(
        "Choose an option:",
        question_data['C'],
        index=None, # No default selection
        key=f"q_{st.session_state.current_question_index}"
    )

    st.session_state.selected_option = selected_option
    
    # Next button to submit the answer
    if st.button("Next", disabled=(selected_option is None)):
        # Find which option was selected (1, 2, or 3)
        choice_index = question_data['C'].index(st.session_state.selected_option) + 1

        # Update scores based on the choice
        if choice_index == 1:
            st.session_state.vata += 1
        elif choice_index == 2:
            st.session_state.pitta += 1
        elif choice_index == 3:
            st.session_state.kapha += 1
        
        # Check if it's the last question
        if st.session_state.current_question_index < len(QUIZ_DATA) - 1:
            st.session_state.current_question_index += 1
        else:
            # End of quiz: calculate result and switch to result view
            st.session_state.prakriti_result = determine_prakriti()
            st.session_state.show_result = True
        
        # Rerun the script to show the next question or the result page
        st.rerun()

# --- Function to display the final results ---
def display_results():
    """Displays the final Prakriti and related advice."""
    st.success(f"Your dominant dosha profile is: **{st.session_state.prakriti_result}**")
    st.info(f"Final Scores: Vata: {st.session_state.vata}, Pitta: {st.session_state.pitta}, Kapha: {st.session_state.kapha}")

    prakriti = st.session_state.prakriti_result
    
    # Determine which dosha details to display
    if prakriti == "Vata":
        doshas_to_display = ["Vata Dosha"]
    elif prakriti == "Pitta":
        doshas_to_display = ["Pitta Dosha"]
    elif prakriti == "Kapha":
        doshas_to_display = ["Kapha Dosha"]
    else: # For dual or tri-dosha results, show all
        doshas_to_display = ["Vata Dosha", "Pitta Dosha", "Kapha Dosha"]
        st.warning("Your result is a combination of doshas. Below are general recommendations for each. For a personalized plan, please consult a qualified Ayurvedic practitioner.")

    for dosha in doshas_to_display:
        with st.expander(f"Recommendations for {dosha}", expanded=True):
            advice = RESULT_DATA[dosha]
            st.markdown(f"**Lifestyle:** {advice['Lifestyle']}")
            st.markdown(f"**Diet:** {advice['Diet']}")
            st.markdown(f"**Wellness:** {advice['Wellness']}")

    st.markdown("---")
    st.markdown("*Disclaimer: This quiz is for educational purposes and is not a substitute for professional medical advice.*")

    # Button to restart the quiz
    if st.button("Try Again"):
        initialize_state()
        st.rerun()

# --- Main App Execution ---
def main():
    st.set_page_config(page_title="Ayurvedic Prakriti Quiz", page_icon="🌿")
    st.title("🌿 Ayurvedic Prakriti Quiz 🌿")
    st.write("Answer the questions to get an insight into your dominant dosha.")
    st.markdown("---")

    # Check if state has been initialized
    if 'current_question_index' not in st.session_state:
        initialize_state()
        
    # Conditional display: show quiz or results
    if st.session_state.show_result:
        display_results()
    else:
        display_quiz()

if __name__ == "__main__":

    main()
