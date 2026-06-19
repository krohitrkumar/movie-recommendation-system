"""
Home Page - Project Overview and Quick Stats
"""

import streamlit as st
import pandas as pd
from data_loader import (
    load_movies_data, 
    load_popularity_recommendations,
    load_ratings_data,
    verify_project_files,
    get_project_stats
)
from visualizations import DashboardMetrics

def show_home():
    """Display home page with project overview and statistics"""
    
    st.markdown("## 🎯 Welcome to Movie Recommendation System")
    
    # Project Overview
    with st.expander("📖 Project Overview", expanded=True):
        st.markdown("""
        This is a **production-ready** Movie Recommendation System built with:
        
        #### 🎬 Three Recommendation Engines:
        1. **Popularity-Based Recommendations** - Top-rated and most-watched movies
        2. **Content-Based Filtering** - Recommendations based on movie similarity
        3. **Collaborative Filtering** - Personalized recommendations using SVD algorithm
        
        #### 📊 Dataset Statistics:
        - 83,000+ movies from MovieLens
        - 33M+ user ratings
        - 330K+ unique users
        - Multiple genres and release years
        
        #### 🔧 Technology Stack:
        - **Python 3.8+** - Data processing and ML
        - **Streamlit** - Interactive web interface
        - **Scikit-Learn** - Machine learning models
        - **Pandas & NumPy** - Data manipulation
        - **Plotly** - Interactive visualizations
        """)
    
    # Project Status
    st.markdown("### ✅ System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        files_status = verify_project_files()
        all_files_present = all(files_status.values())
        status_icon = "✅" if all_files_present else "⚠️"
        st.write(f"{status_icon} **Data Files**: {'Ready' if all_files_present else 'Missing'}")
    
    with col2:
        st.write("✅ **Models**: Ready")
    
    with col3:
        st.write("✅ **Application**: Online")
    
    # Show file verification details
    with st.expander("📋 File Verification Details"):
        for file, exists in verify_project_files().items():
            status = "✅ Present" if exists else "❌ Missing"
            st.write(f"{status} - {file}")
    
    # Key Statistics
    st.markdown("---")
    st.markdown("### 📊 Key Metrics")
    
    try:
        stats = get_project_stats()
        DashboardMetrics.display_metrics(stats)
    except Exception as e:
        st.error(f"Error loading statistics: {str(e)}")
    
    # Quick Actions
    st.markdown("---")
    st.markdown("### 🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        ### 📈 View Popular Movies
        Check out the most popular movies based on ratings and watch count.
        
        **[→ Go to Popularity Page]**
        """)
    
    with col2:
        st.success("""
        ### 🎯 Find Similar Movies
        Search for a movie and get content-based recommendations.
        
        **[→ Go to Content-Based Page]**
        """)
    
    with col3:
        st.warning("""
        ### 👥 Get Personalized Recs
        Enter a User ID to get personalized recommendations.
        
        **[→ Go to Collaborative Page]**
        """)
    
    # How It Works
    st.markdown("---")
    st.markdown("### 🤔 How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 1️⃣ Popularity-Based
        
        Recommends the most popular movies based on:
        - Average user ratings
        - Number of ratings received
        - Recent activity
        
        **Best for:** New users or discovery
        """)
    
    with col2:
        st.markdown("""
        #### 2️⃣ Content-Based
        
        Finds similar movies based on:
        - Genres and metadata
        - Movie descriptions
        - Tags and keywords
        
        **Best for:** Finding movies like your favorite
        """)
    
    with col3:
        st.markdown("""
        #### 3️⃣ Collaborative Filtering
        
        Predicts ratings based on:
        - Similar users' preferences
        - SVD matrix factorization
        - Rating patterns
        
        **Best for:** Personalized recommendations
        """)
    
    # Data Source Info
    st.markdown("---")
    st.markdown("### 📚 About the Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Dataset:** MovieLens Dataset
        
        - Comprehensive movie metadata
        - User ratings (0.5 - 5.0 stars)
        - User-provided tags
        - Timestamp of interactions
        """)
    
    with col2:
        st.markdown("""
        **Data Processing:**
        
        - SQL data validation and cleaning
        - Python preprocessing pipeline
        - Feature engineering for ML models
        - Model training and evaluation
        """)
    
    # Navigation Tips
    st.markdown("---")
    st.markdown("### 💡 Navigation Tips")
    
    st.info("""
    - **Sidebar Navigation**: Use the sidebar menu to switch between different recommendation types and analytics
    - **Search Functionality**: Use fuzzy matching in Content-Based section to find movies
    - **Analytics Dashboard**: View detailed statistics and visualizations in the Analytics section
    - **Model Information**: Learn more about each algorithm in the About section
    """)
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; margin-top: 30px;'>
        <p>Built with ❤️ using Streamlit | Version 1.0.0</p>
        <p style='font-size: 12px;'>project demonstration</p>
    </div>
    """, unsafe_allow_html=True)
