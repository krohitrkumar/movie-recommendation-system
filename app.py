"""
Smart Movie Recommender
Movie Recommendation System using
Popularity-Based, Content-Based, and Collaborative Filtering.
"""

import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="🎥 Smart Movie Recommender",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com",
        "Report a bug": "https://github.com",
        "About": "# Smart Movie Recommender\n\nMovie recommendation platform powered by intelligent recommendation algorithms."
    }
)

# Session State
if "app_initialized" not in st.session_state:
    st.session_state.app_initialized = True
    st.session_state.selected_page = "Home"
    st.session_state.search_history = []

# Custom CSS
st.markdown("""
<style> 
.recommendation-card {
    background-color: #f0f2f6;
    padding: 20px;
    border-radius: 10px;
    margin: 10px 0;
    border-left: 5px solid #ff6b6b;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.metric-card {
    background-color: #e3f2fd;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    text-align: center;
}

.header-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 10px;
    color: white;
    margin-bottom: 20px;
}

h1 {
    color: #667eea;
}

h2 {
    color: #764ba2;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:

    st.markdown("### 🎥 Navigation")

    pages = {
        "🏠 Home": "pages/Home",
        "📊 Popularity-Based": "pages/Popularity",
        "🎯 Content-Based": "pages/Content_Based",
        "👥 Collaborative Filtering": "pages/Collaborative_Filtering",
        "📈 Analytics": "pages/Analytics",
        "ℹ️ About": "pages/About"
    }

    selected = st.radio(
        "Select Page",
        list(pages.keys()),
        key="navigation"
    )

    st.markdown("---")

    st.markdown("### Recommendation Methods")

    st.info("""
📊 Popularity-Based

🎯 Content-Based

👥 Collaborative Filtering
""")

# Header
st.markdown("""
<div class="header-container">
    <h1>🎥 Smart Movie Recommender</h1>
    <p>Discover personalized movie recommendations using intelligent recommendation algorithms.</p>
</div>
""", unsafe_allow_html=True)

# Page Routing
if selected == "🏠 Home":
    from pages.Home import show_home
    show_home()

elif selected == "📊 Popularity-Based":
    from pages.Popularity import show_popularity
    show_popularity()

elif selected == "🎯 Content-Based":
    from pages.Content_Based import show_content_based
    show_content_based()

elif selected == "👥 Collaborative Filtering":
    from pages.Collaborative_Filtering import show_collaborative_filtering
    show_collaborative_filtering()

elif selected == "📈 Analytics":
    from pages.Analytics import show_analytics
    show_analytics()

elif selected == "ℹ️ About":
    from pages.About import show_about
    show_about()

# Footer
st.markdown("---")

st.markdown("""
<div style='text-align:center;color:gray;margin-top:40px;'>
    <p>🎥 Smart Movie Recommender</p>
</div>
""", unsafe_allow_html=True)
