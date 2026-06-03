"""
About Page - Project Information and Documentation
"""

import streamlit as st
from data_loader import verify_project_files

def show_about():
    """Display about page with project information"""
    
    st.markdown("## ℹ️ About This Project")
    
    # Project Overview
    with st.expander("🎬 Project Overview", expanded=True):
        st.markdown("""
        # Movie Recommendation System
        
        A **production-ready** end-to-end movie recommendation system demonstrating
        multiple machine learning approaches for personalized content discovery.
        
        **Built for:**  Project Demonstration | Portfolio
        
        **Status:** ✅ Production-Ready
        """)
    
    # Technology Stack
    with st.expander("🔧 Technology Stack", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Backend")
            st.write("""
            - **Python 3.8+**
            - **Pandas** - Data manipulation
            - **NumPy** - Numerical computing
            - **Scikit-Learn** - ML algorithms
            - **Surprise** - Recommendation library
            """)
        
        with col2:
            st.markdown("### Frontend")
            st.write("""
            - **Streamlit** - Web framework
            - **Plotly** - Interactive charts
            - **Plotly Express** - Visualization
            - **Custom CSS** - Styling
            """)
        
        with col3:
            st.markdown("### Data & Infrastructure")
            st.write("""
            - **PostgreSQL** - Database
            - **SQLAlchemy** - ORM
            - **Jupyter** - Development
            - **Git** - Version control
            """)
    
    # Recommendation Algorithms
    with st.expander("🤖 Recommendation Algorithms", expanded=False):
        st.markdown("### Three Recommendation Approaches:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 1. Popularity-Based")
            st.write("""
            **Algorithm:**
            - Rank by average rating
            - Weight by review count
            - Simple yet effective
            
            **Pros:**
            - Works for cold-start users
            - Highlights quality content
            - Easy to interpret
            
            **Cons:**
            - Lacks personalization
            - Favors popular items
            """)
        
        with col2:
            st.markdown("#### 2. Content-Based")
            st.write("""
            **Algorithm:**
            - TF-IDF vectorization
            - Cosine similarity
            - Genre & metadata matching
            
            **Pros:**
            - No user data needed
            - Transparent reasoning
            - Avoids popularity bias
            
            **Cons:**
            - Limited serendipity
            - Feature engineering crucial
            """)
        
        with col3:
            st.markdown("#### 3. Collaborative Filtering")
            st.write("""
            **Algorithm:**
            - SVD matrix factorization
            - Latent factor modeling
            - User-item interactions
            
            **Pros:**
            - Captures complex patterns
            - Discovers unexpected gems
            - Highly personalized
            
            **Cons:**
            - Cold-start for new users
            - Popularity bias possible
            """)
    
    # Dataset Information
    with st.expander("📊 Dataset Information", expanded=False):
        st.markdown("### MovieLens Dataset")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Size & Scale:**")
            st.write("""
            - 83,000+ movies
            - 33,000,000+ ratings
            - 330,000+ users
            - Multiple decades of data
            """)
        
        with col2:
            st.markdown("**Data Types:**")
            st.write("""
            - Movie metadata (title, year, genres)
            - User ratings (0.5 - 5.0 stars)
            - Tags and descriptions
            - Temporal information
            """)
        
        st.markdown("**Data Processing Pipeline:**")
        
        stages = {
            "1. SQL Setup": "Database schema creation and indexing",
            "2. Data Loading": "ETL from raw files to PostgreSQL",
            "3. Validation": "Data quality checks and cleaning",
            "4. Preprocessing": "Feature engineering and normalization",
            "5. Analysis": "EDA and statistical exploration",
            "6. Modeling": "Training ML models and evaluation",
        }
        
        for stage, description in stages.items():
            st.write(f"**{stage}**: {description}")
    
    # Project Structure
    with st.expander("📁 Project Structure", expanded=False):
        st.markdown("""
        ```
        movie_recommendation_project/
        │
        ├── 0.data/                          # Raw data files
        │   ├── movies.csv
        │   ├── ratings.csv
        │   ├── tags.csv
        │   └── links.csv
        │
        ├── 1.sql/                           # SQL scripts
        │   ├── 01_database_setup.sql
        │   ├── 02_load_data.sql
        │   ├── 03_validation.sql
        │   ├── 04_data_preparation.sql
        │   └── 05_eda.sql
        │
        ├── 2.notebook/                      # Jupyter notebooks
        │   ├── 01_database_connection.ipynb
        │   ├── 02_python_preprocessing.ipynb
        │   ├── 03_visualization_eda.ipynb
        │   └── 04_recommendation_system.ipynb
        │
        ├── 3.outputs/                       # Processed data
        │   ├── movies_processed.csv
        │   ├── ratings_processed.csv
        │   ├── tags_processed.csv
        │   └── popularity_based_recommendation.csv
        │
        ├── 4.models/                        # Trained models
        │   ├── movie_content_recommender.pkl
        │   └── collaborative_filtering_svd.pkl
        │
        ├── 5.visualizations/                # Generated charts
        │   ├── rating_distribution.html
        │   ├── top_genres.html
        │   └── ...
        │
        ├── pages/                           # Streamlit pages
        │   ├── Home.py
        │   ├── Popularity.py
        │   ├── Content_Based.py
        │   ├── Collaborative_Filtering.py
        │   ├── Analytics.py
        │   └── About.py
        │
        ├── app.py                           # Main Streamlit app
        ├── data_loader.py                   # Data loading utilities
        ├── recommenders.py                  # Recommendation engines
        ├── visualizations.py                # Visualization utilities
        ├── requirements.txt                 # Dependencies
        ├── .env                            # Environment variables
        ├── .gitignore                      # Git ignore rules
        └── README.md                       # Project documentation
        ```
        """)
    
    # File Verification
    with st.expander("✅ System Health Check", expanded=False):
        st.markdown("### File Verification")
        
        files_status = verify_project_files()
        
        for file, exists in files_status.items():
            status = "✅ Present" if exists else "❌ Missing"
            st.write(f"{status} - `{file}`")
        
        all_good = all(files_status.values())
        
        if all_good:
            st.success("✅ All required files present and ready!")
        else:
            st.warning("⚠️ Some files are missing. Check paths and try running the notebooks.")
    
    # Performance Considerations
    with st.expander("⚡ Performance & Optimization", expanded=False):
        st.markdown("""
        ### Memory-Efficient Design
        
        **Strategies Implemented:**
        - Streamlit caching for data and models (@st.cache_data, @st.cache_resource)
        - On-demand model loading
        - Sample-based analysis for large datasets
        - Lazy evaluation of visualizations
        - Session state management
        
        **Resource Usage:**
        - Content model: ~80MB (TF-IDF matrices)
        - Collaborative model: ~1.1GB (SVD factors)
        - Data cache: ~500MB (sampled data)
        
        **Optimization Tips:**
        - First load creates cache (may take 10-30 seconds)
        - Subsequent loads are instant
        - Toggle sampling in Analytics for faster processing
        - Use filters to reduce data in visualizations
        """)
    
    # Deployment Guide
    with st.expander("🚀 Deployment Instructions", expanded=False):
        st.markdown("""
        ### Local Development
        
        ```bash
        # 1. Clone repository
        git clone <repository-url>
        cd movie_recommendation_project
        
        # 2. Create virtual environment
        python -m venv venv
        source venv/bin/activate  # On Windows: venv\\Scripts\\activate
        
        # 3. Install dependencies
        pip install -r requirements.txt
        
        # 4. Configure environment
        cp .env.example .env
        # Edit .env with your database credentials
        
        # 5. Run Streamlit app
        streamlit run app.py
        ```
        
        **Access the app:**
        - Local: http://localhost:8501
        - Network: Available on local IP address
        
        ### Streamlit Cloud Deployment
        
        ```bash
        # 1. Push to GitHub
        git push origin main
        
        # 2. Go to streamlit.io/cloud
        # 3. Connect GitHub repository
        # 4. Deploy main branch
        # 5. Configure secrets in Streamlit Cloud
        ```
        
        **Required Environment Variables:**
        - DB_USER: PostgreSQL username
        - DB_PASSWORD: PostgreSQL password
        - DB_HOST: Database host
        - DB_PORT: Database port (default 5432)
        - DB_NAME: Database name
        """)
    
    # Features & Highlights
    with st.expander("✨ Key Features", expanded=False):
        st.markdown("""
        ### Application Features
        
        ✅ **Multi-Page Layout**
        - Sidebar navigation
        - Seamless page switching
        - Session state management
        
        ✅ **Search Capabilities**
        - Fuzzy matching for movie titles
        - Partial title search
        - Autocomplete suggestions
        - Closest match recommendations
        
        ✅ **Recommendation Systems**
        - Popularity-based rankings
        - Content-based filtering
        - Collaborative filtering (SVD)
        - Explanation of recommendations
        
        ✅ **Interactive Visualizations**
        - Rating distributions
        - Genre analysis
        - Trend tracking
        - Export to HTML
        
        ✅ **Analytics Dashboard**
        - Key metrics display
        - Comparative analysis
        - Data export functionality
        - Statistics reporting
        
        ✅ **Best Practices**
        - Streamlit caching optimization
        - Error handling and recovery
        - Loading indicators
        - Responsive design
        """)
    
    # Troubleshooting
    with st.expander("🔧 Troubleshooting", expanded=False):
        st.markdown("""
        ### Common Issues & Solutions
        
        **Issue: Model files not found**
        - Solution: Ensure model files exist in `4.models/` folder
        - Check: `4.models/movie_content_recommender.pkl` and `collaborative_filtering_svd.pkl`
        
        **Issue: CSV files not loading**
        - Solution: Verify CSV files in `3.outputs/` folder
        - Check: File names and paths are correct
        
        **Issue: Slow performance on first load**
        - Solution: This is normal - data and models are being cached
        - Subsequent loads will be instant
        
        **Issue: Memory errors**
        - Solution: The app uses sampling for large datasets
        - Reduce sample size in Analytics settings
        
        **Issue: Search returns no results**
        - Solution: Use partial titles or fuzzy matching
        - Try different spellings or keywords
        """)
    
    # Credits & References
    with st.expander("📚 Credits & References", expanded=False):
        st.markdown("""
        ### Project Credits
        
        **Dataset:**
        - MovieLens dataset by GroupLens Research
        - https://grouplens.org/datasets/movielens/
        
        **Technologies:**
        - Streamlit: https://streamlit.io/
        - Scikit-Learn: https://scikit-learn.org/
        - Plotly: https://plotly.com/
        
        **Algorithms & Papers:**
        - Koren, Y. et al. (2009): "Matrix Factorization Techniques for Recommender Systems"
        - Sarwar, B. et al. (2001): "Item-based collaborative filtering recommendation algorithms"
        
        **Developed for:**
        - Project Demonstration
        - Portfolio Showcase
        - Educational Purpose
        """)
    
    # Contact & Support
    st.markdown("---")
    st.markdown("### 📞 Support & Feedback")
    st.info("""
    **Questions or Issues?**
    - Check the GitHub repository issues page
    - Review the troubleshooting section above
    - Test with example user IDs and movies
    
    **Contributing:**
    - Fork the repository
    - Create feature branches
    - Submit pull requests
    - Report bugs via issues
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>🎬 Movie Recommendation System</p>
        <p style='font-size: 12px;'>Built with Streamlit | Powered by Machine Learning</p>
        <p style='font-size: 11px;'>© 2026 - Educational Project</p>
    </div>
    """, unsafe_allow_html=True)
