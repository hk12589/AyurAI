import streamlit as st
from pathlib import Path

# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="AyurAI Blogs",
    page_icon="🌿",
    layout="wide"
)

# ==============================================================================
# Data for Blog Posts
# image_path points to local files in the 'img' folder.
# The 'link' corresponds to the filename in the 'pages' directory (without the number/emoji prefix and .py extension).
# ==============================================================================
BLOG_POSTS = [
    {
        "title": "Yoga and Ayurveda: A Perfect Synergy 🧘‍♀️🌿",
        "description": "Welcome to our comprehensive guide on the beautiful synergy between Yoga and Ayurveda...",
        "image_path": "img/1.jpg",
        "link": "Yoga_and_Ayurveda_blog_page"
    },
    {
        "title": "Top 10 Ayurvedic Herbs for Daily Health 🌿✨",
        "description": "Welcome to our comprehensive guide on the Top 10 Ayurvedic Herbs for your daily wellness routine...",
        "image_path": "img/2.jpg",
        "link": "Top_10_Ayurvedic_Herbs_Blog_Page" # Placeholder link for other blogs
    },
    {
        "title": "Ayurvedic Diet: Eating According to Your Dosha 🍽️�",
        "description": "Welcome to our comprehensive guide on the Ayurvedic Diet, where we explore eating for your dosha...",
        "image_path": "img/3.jpg",
        "link": "Ayurvedic_Diet_Blog_Page"
    },
    {
        "title": "Integrating Ayurveda with Modern Medical Treatments 🌟",
        "description": "Ayurveda and modern medicine have unique strengths that can complement each other for holistic health...",
        "image_path": "img/4.jpg",
        "link": "Holistic_Healing_Blog_Page"
    },
    {
        "title": "Seasonal Ayurvedic Practices: Staying Healthy All Year 🌿🕰️",
        "description": "Ayurveda emphasizes living in harmony with the natural rhythms of the seasons to maintain balance...",
        "image_path": "img/5.jpg",
        "link": "Seasonal_Ayurvedic_Practices_Blog_Page"
    },
    {
        "title": "Managing Stress with Ayurveda 🌿🧘‍♀️",
        "description": "Meditation is a powerful Ayurvedic practice that calms the mind and reduces the effects of stress...",
        "image_path": "img/6.jpg",
        "link": "Managing_Stress_with_Ayurveda_Blog_Page"
    },
    {
        "title": "Detoxing the Ayurvedic Way: Panchakarma Explained 🌿✨",
        "description": "Panchakarma, which translates to 'five actions' in Sanskrit, is the ultimate Ayurvedic detoxification...",
        "image_path": "img/7.jpg",
        "link": "Detoxing_the_Ayurvedic_Way_Blog_Page"
    },
    {
        "title": "Ayurvedic Beauty Secrets: Natural Ways to Glow 🌿✨",
        "description": "Abhyanga is a daily self-massage practice using warm oil to nourish the skin and calm the nervous system...",
        "image_path": "img/8.jpg",
        "link": "Ayurvedic_Beauty_Secrets_Blog_Page"
    }
]

# ==============================================================================
# Streamlit UI Layout
# ==============================================================================

st.title("AyurAI Blogs")
st.markdown("---")

# Create a grid layout with 4 columns for better spacing
cols = st.columns(4)
col_index = 0

# Loop through the blog posts and display them in cards
for post in BLOG_POSTS:
    # Use the 'with' statement to place content in the current column
    with cols[col_index]:
        # Use st.container with a border to create a card effect
        with st.container(border=True):
            # Display the image directly from the local path
            if Path(post["image_path"]).is_file():
                st.image(post["image_path"], use_container_width=True)
            else:
                # Show a placeholder if the image is not found
                st.image("https://placehold.co/600x400/ccc/333?text=Image+Not+Found", use_container_width=True)

            # Add title and description
            st.subheader(post["title"])
            st.write(post["description"])

            # Add a "Read More" button that links to the page
            # The button is disabled if the link is just a placeholder
            st.link_button("Read More →", post["link"], disabled=(post["link"] == "#"))

    # Move to the next column, and wrap around to the start if necessary
    col_index = (col_index + 1) % 4