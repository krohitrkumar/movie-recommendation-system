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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Apply modern typography */
html, body, [class*="css"], .stMarkdown {
    font-family: 'Inter', sans-serif !important;
}

/* Business slate header container */
.header-container {
    background: #0f172a;
    padding: 2rem;
    border-radius: 12px;
    color: white;
    margin-bottom: 2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    text-align: left;
    border-left: 6px solid #2563eb;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.header-container h1 {
    color: #f8fafc !important;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    margin-top: 0 !important;
    margin-bottom: 0.5rem !important;
}

.header-container p {
    font-size: 1rem;
    color: #94a3b8;
    font-weight: 400;
    margin: 0 !important;
}

/* Premium Slate Cards */
.movie-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 1.25rem;
    margin: 0.75rem 0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    border-left: 5px solid #2563eb;
}

.movie-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    border-left-color: #10b981;
    background: #243249;
}

/* Metric Cards for Business Intelligence Style */
div[data-testid="metric-container"] {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-left: 4px solid #2563eb !important;
    padding: 1rem !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
    transition: all 0.2s ease !important;
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-2px) !important;
    border-color: #3b82f6 !important;
    border-left-color: #10b981 !important;
}

div[data-testid="stMetricValue"] {
    font-size: 1.7rem !important;
    font-weight: 700 !important;
    color: #3b82f6 !important;
}

/* Genre badge tags */
.genre-badge {
    background: rgba(59, 130, 246, 0.12);
    color: #60a5fa;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 500;
    display: inline-block;
    margin-right: 5px;
    border: 1px solid rgba(59, 130, 246, 0.2);
}

/* Sidebar auto navigation list suppression */
[data-testid="stSidebarNav"] {
    display: none !important;
}

/* Style main headings */
h1 {
    color: #f8fafc !important;
    font-weight: 700 !important;
}

h2 {
    color: #3b82f6 !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:

    st.markdown("### 📽️ Dashboard Navigation")

    pages = {
        "🏠 Home": "app_pages/Home",
        "📊 Popularity-Based": "app_pages/Popularity",
        "🎯 Content-Based": "app_pages/Content_Based",
        "👥 Collaborative Filtering": "app_pages/Collaborative_Filtering",
        "📈 Analytics": "app_pages/Analytics",
        "ℹ️ About": "app_pages/About"
    }

    selected = st.radio(
        "Select Page",
        list(pages.keys()),
        key="navigation"
    )

    st.markdown("---")

    st.markdown("### ⚡ Live Model Engines")
    st.markdown("""
    <div style="font-size: 0.9rem; line-height: 1.6;">
        <span style="color: #10b981;">●</span> <b>Popularity Engine</b>: <span style="color: #10b981; font-weight: 600;">Active</span><br>
        <span style="color: #10b981;">●</span> <b>Content Engine</b>: <span style="color: #10b981; font-weight: 600;">Active</span><br>
        <span style="color: #10b981;">●</span> <b>Collaborative Engine</b>: <span style="color: #10b981; font-weight: 600;">Active</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📊 Database Volume")
    st.markdown("""
    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 0.75rem; font-size: 0.85rem; line-height: 1.5; color: #cbd5e1;">
        🗄️ <b>Total Movies</b>: 83,000+<br>
        ⭐ <b>Total Ratings</b>: 33,000,000+<br>
        👥 <b>Unique Users</b>: 330,000+
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Active Session Properties
    user_id = st.session_state.get("selected_user", "None")
    st.markdown("### 🔑 Active Session")
    st.markdown(f"""
    <div style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.6;">
        👤 <b>Active User ID</b>: <code style="color: #60a5fa; background: #1e293b; padding: 2px 6px; border-radius: 4px; border: 1px solid #334155;">{user_id}</code><br>
    </div>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <h1>🎥 Smart Movie Recommender</h1>
    <p>Discover personalized movie recommendations using intelligent recommendation algorithms.</p>
</div>
""", unsafe_allow_html=True)

# Page Routing
if selected == "🏠 Home":
    from app_pages.Home import show_home
    show_home()

elif selected == "📊 Popularity-Based":
    from app_pages.Popularity import show_popularity
    show_popularity()

elif selected == "🎯 Content-Based":
    from app_pages.Content_Based import show_content_based
    show_content_based()

elif selected == "👥 Collaborative Filtering":
    from app_pages.Collaborative_Filtering import show_collaborative_filtering
    show_collaborative_filtering()

elif selected == "📈 Analytics":
    from app_pages.Analytics import show_analytics
    show_analytics()

elif selected == "ℹ️ About":
    from app_pages.About import show_about
    show_about()

# Footer
st.markdown("---")

st.markdown("""
<div style='text-align:center;color:gray;margin-top:40px;'>
    <p>🎥 Smart Movie Recommender</p>
</div>
""", unsafe_allow_html=True)
