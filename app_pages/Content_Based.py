"""
Content-Based Recommendations Page
Find similar movies based on content features
"""

import streamlit as st
import pandas as pd
from data_loader import load_movies_data, load_content_recommender
from recommenders import create_movie_search_engine, create_content_recommender
from visualizations import RecommendationDisplay

def show_content_based():
    """Display content-based recommendations"""
    
    st.markdown("## 🎯 Content-Based Recommendations")
    st.markdown("""
    Find movies similar to ones you like, based on **genres, keywords, and metadata**.
    The algorithm analyzes movie features and finds similar titles.
    """)
    
    # Load data and models
    with st.spinner("Loading data and models..."):
        movies_df = load_movies_data()
        model = load_content_recommender()
    
    if movies_df.empty:
        st.error("Could not load movie data.")
        return
    
    if model is None:
        st.error("Could not load content-based recommendation model.")
        st.info("Please ensure the model file exists: 4.models/movie_content_recommender.pkl")
        return
    
    # Create search engine and recommender
    search_engine = create_movie_search_engine(movies_df)
    recommender = create_content_recommender(model, movies_df)
    
    # Sidebar controls
    with st.sidebar:
        st.markdown("### ⚙️ Recommendation Settings")
        n_recommendations = st.slider(
            "Number of Recommendations",
            min_value=3,
            max_value=20,
            value=10,
            step=1
        )
        
        threshold = st.slider(
            "Search Sensitivity",
            min_value=0.3,
            max_value=0.9,
            value=0.6,
            step=0.1,
            help="Higher = stricter matching"
        )
    
    # Main content
    st.markdown("### 🔍 Search for a Movie")
    
    # Initialize search state if set by suggestions or random browser
    default_search = ""
    if "selected_suggestion" in st.session_state and st.session_state.selected_suggestion:
        default_search = st.session_state.selected_suggestion
        st.session_state.selected_suggestion = None  # Clear it
    elif "quick_search" in st.session_state and st.session_state.quick_search:
        default_search = st.session_state.quick_search
        st.session_state.quick_search = None  # Clear it
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Enter a movie title (or partial title)",
            value=default_search,
            placeholder="e.g., 'Inception', 'Dark Knight', 'Avatar'..."
        )
    
    with col2:
        search_button = st.button("🔍 Search", width="stretch")
    
    if search_query or search_button:
        if not search_query.strip():
            st.warning("Please enter a movie title to search.")
        else:
            # Search for movie
            movie, suggestions = search_engine.search(search_query)
            
            if movie is not None:
                # Movie found
                st.markdown("---")
                st.markdown("### ✅ Movie Found!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Title", movie['title'])
                with col2:
                    st.metric("Year", int(movie['release_year']))
                with col3:
                    st.metric("Genres", movie['genres'])
                
                st.markdown("---")
                st.markdown(f"### 📽️ Similar Movies to '{movie['title']}'")
                
                # Get recommendations
                with st.spinner("Finding similar movies..."):
                    recommendations = recommender.get_recommendations(
                        movie['title'],
                        n=n_recommendations
                    )
                
                if not recommendations.empty:
                    st.success(f"Found {len(recommendations)} similar movies!")
                    
                    # Display recommendations
                    for idx, row in recommendations.iterrows():
                        # Format genres nicely as tags
                        genres_html = ""
                        if pd.notna(row.get('genres')):
                            genres_list = [g.strip() for g in row['genres'].split('|')]
                            genres_html = " ".join([f'<span class="genre-badge">{g}</span>' for g in genres_list])
                        
                        year_str = f"({int(row['release_year'])})" if pd.notna(row.get('release_year')) else ""
                        
                        st.markdown(f"""
                        <div class="movie-card">
                            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                                <div style="flex: 2; min-width: 250px;">
                                    <h3 style="margin: 0 0 0.5rem 0; font-size: 1.4rem; color: #f8fafc;">🎬 {row['title']} <span style="font-weight: 300; opacity: 0.6; color: #94a3b8;">{year_str}</span></h3>
                                    <div style="display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 0.2rem;">{genres_html}</div>
                                </div>
                                <div style="flex: 1; min-width: 200px; display: flex; gap: 0.8rem; justify-content: flex-end; align-items: center;">
                                    <div style="text-align: center; background: rgba(37, 99, 235, 0.12); padding: 0.4rem 0.8rem; border-radius: 8px; border: 1px solid rgba(37, 99, 235, 0.25); min-width: 100px;">
                                        <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.5px; color: #60a5fa; font-weight: 500;">Similarity</div>
                                        <div style="font-size: 1.15rem; font-weight: 700; color: #3b82f6;">{row['similarity_score']:.2%}</div>
                                    </div>
                                    <div style="text-align: center; background: rgba(16, 185, 129, 0.12); padding: 0.4rem 0.8rem; border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.25); min-width: 90px;">
                                        <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.5px; color: #34d399; font-weight: 500;">Cos Score</div>
                                        <div style="font-size: 1.15rem; font-weight: 700; color: #10b981;">{row['similarity_score']:.3f}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No similar movies found. Try a different movie.")
            else:
                # No exact match, show suggestions
                st.markdown("---")
                st.markdown("### 🤔 Movie Not Found")
                st.info(f"Could not find an exact match for '{search_query}'")
                
                if suggestions:
                    st.markdown("### 💡 Did you mean?")
                    
                    # Create columns for suggestions
                    cols = st.columns(min(3, len(suggestions)))
                    
                    for idx, suggestion in enumerate(suggestions[:3]):
                        with cols[idx]:
                            if st.button(suggestion, key=f"suggestion_{idx}", width="stretch"):
                                st.session_state.selected_suggestion = suggestion
                                st.rerun()
                    
                    st.markdown("---")
                    st.markdown("### 📊 Search Tips:")
                    st.info("""
                    - Try partial titles (e.g., "Dark" instead of "The Dark Knight")
                    - Check your spelling
                    - Browse popular movies in the Popularity tab
                    - Use different keywords
                    """)
    
    # Browse mode
    st.markdown("---")
    st.markdown("### 📚 Browse Movies")
    
    if st.checkbox("Show random movies for recommendation"):
        n_random = st.slider("How many random movies?", 3, 20, 5)
        
        # Initialize or update random movies cache in session state
        if "random_movies_list" not in st.session_state or len(st.session_state.random_movies_list) != n_random:
            st.session_state.random_movies_list = movies_df.sample(n=n_random)
            
        if st.button("🔄 Refresh Random List", width="stretch"):
            st.session_state.random_movies_list = movies_df.sample(n=n_random)
            st.rerun()
            
        random_movies = st.session_state.random_movies_list
        st.markdown(f"#### Random Movies (sample of {n_random})")
        
        for idx, row in random_movies.iterrows():
            col1, col2 = st.columns([3, 1])
            
            year_val = f"({int(row['release_year'])})" if pd.notna(row.get('release_year')) and row['release_year'] > 0 else ""
            with col1:
                st.markdown(f"**{row['title']}** {year_val}")
                st.write(f"Genres: {row['genres']}")
            
            with col2:
                if st.button("Get Recommendations", key=f"quick_{idx}"):
                    st.session_state.quick_search = row['title']
                    st.rerun()
    
    # Algorithm explanation
    st.markdown("---")
    st.markdown("""
    ### 📌 How This Works
    
    **Content-Based Filtering:**
    1. Analyzes movie features (genres, keywords, metadata)
    2. Represents each movie as a feature vector
    3. Calculates similarity between movies using TF-IDF and cosine similarity
    4. Finds movies most similar to your selection
    
    **Algorithm Details:**
    - **TF-IDF Vectorization**: Converts movie metadata into numerical features
    - **Cosine Similarity**: Measures angle between feature vectors
    - **Top-K Selection**: Returns k most similar movies
    
    **Advantages:**
    - Works without user ratings data
    - Finds hidden gems similar to known good movies
    - Interpretable recommendations (you know why)
    - No cold-start problem for new movies
    
    **Use Cases:**
    - Finding movies similar to your favorites
    - Discovering movies in your preferred genre
    - Exploring director/actor filmographies
    """)
