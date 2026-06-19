"""
Collaborative Filtering Recommendations Page
Personalized recommendations using SVD matrix factorization
"""

import streamlit as st
import pandas as pd
import numpy as np
from data_loader import load_movies_data, load_collaborative_filtering_model, load_ratings_data
from recommenders import create_collaborative_recommender

def show_collaborative_filtering():
    """Display collaborative filtering recommendations"""
    
    st.markdown("## 👥 Collaborative Filtering Recommendations")
    st.markdown("""
    Get **personalized recommendations** based on similar users' preferences.
    Using matrix factorization (SVD) to predict your movie ratings!
    """)
    
    # Load data and models
    with st.spinner("Loading data and models..."):
        movies_df = load_movies_data()
        model = load_collaborative_filtering_model()
        ratings_sample = load_ratings_data(sample=50000)
    
    if movies_df.empty:
        st.error("Could not load movie data.")
        return
    
    if model is None:
        st.error("Could not load collaborative filtering model.")
        st.info("Please ensure the model file exists: 4.models/collaborative_filtering_svd.pkl")
        return
    
    # Create recommender
    recommender = create_collaborative_recommender(model, movies_df)
    
    # Sidebar controls
    with st.sidebar:
        st.markdown("### ⚙️ Recommendation Settings")
        n_recommendations = st.slider(
            "Number of Recommendations",
            min_value=5,
            max_value=30,
            value=10,
            step=1
        )
        
        min_predicted_rating = st.slider(
            "Minimum Predicted Rating",
            min_value=0.0,
            max_value=5.0,
            value=3.0,
            step=0.5,
            help="Show only movies predicted to have this rating or higher"
        )
    
    # Main content
    st.markdown("### 👤 Enter Your User ID")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_id_input = st.text_input(
            "Enter a User ID (integer)",
            placeholder="e.g., 1, 42, 1000...",
            value=str(st.session_state.get("selected_user", ""))
        )
    
    with col2:
        recommend_button = st.button("🚀 Get Recommendations", width="stretch")
    
    if user_id_input or recommend_button:
        if not user_id_input.strip():
            st.warning("Please enter a valid User ID (must be a number).")
        else:
            try:
                user_id = int(user_id_input.strip())
                
                # Validate user ID
                if user_id <= 0:
                    st.error("User ID must be a positive integer.")
                else:
                    st.markdown("---")
                    
                    # Get recommendations
                    with st.spinner(f"Generating personalized recommendations for User {user_id}..."):
                        recommendations = recommender.get_recommendations(
                            user_id,
                            n=n_recommendations
                        )
                    
                    if not recommendations.empty:
                        # Filter by minimum rating
                        filtered_recs = recommendations[
                            recommendations['predicted_rating'] >= min_predicted_rating
                        ]
                        
                        if not filtered_recs.empty:
                            st.success(f"✅ Found {len(filtered_recs)} personalized recommendations!")
                            
                            # Display user info
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("User ID", user_id)
                            with col2:
                                st.metric("Recommendations", len(filtered_recs))
                            with col3:
                                avg_rating = filtered_recs['predicted_rating'].mean()
                                st.metric("Avg Predicted Rating", f"{avg_rating:.2f}/5.0")
                            
                            st.markdown("---")
                            st.markdown("### 🎬 Your Personalized Movie Recommendations")
                            
                            # Display recommendations
                            for idx, row in filtered_recs.iterrows():
                                # Format genres nicely as tags
                                genres_html = ""
                                if pd.notna(row.get('genres')):
                                    genres_list = [g.strip() for g in row['genres'].split('|')]
                                    genres_html = " ".join([f'<span class="genre-badge">{g}</span>' for g in genres_list])
                                
                                year_str = f"({int(row['release_year'])})" if pd.notna(row.get('release_year')) else ""
                                confidence = min(100, max(0, (row['predicted_rating'] - 3) * 20 + 50))
                                
                                st.markdown(f"""
                                <div class="movie-card">
                                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                                        <div style="flex: 2; min-width: 250px;">
                                            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.4rem; color: #f8fafc;">🎬 {row['title']} <span style="font-weight: 300; opacity: 0.6; color: #94a3b8;">{year_str}</span></h3>
                                            <div style="display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 0.5rem;">{genres_html}</div>
                                            <div style="font-size: 0.9rem; color: #94a3b8; font-style: italic;">We predict you'll rate this {row['predicted_rating']:.1f}/5</div>
                                        </div>
                                        <div style="flex: 1; min-width: 200px; display: flex; gap: 0.8rem; justify-content: flex-end; align-items: center;">
                                            <div style="text-align: center; background: rgba(37, 99, 235, 0.12); padding: 0.4rem 0.8rem; border-radius: 8px; border: 1px solid rgba(37, 99, 235, 0.25); min-width: 90px;">
                                                <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.5px; color: #60a5fa; font-weight: 500;">Prediction</div>
                                                <div style="font-size: 1.15rem; font-weight: 700; color: #3b82f6;">{row['predicted_rating']:.2f}</div>
                                            </div>
                                            <div style="text-align: center; background: rgba(16, 185, 129, 0.12); padding: 0.4rem 0.8rem; border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.25); min-width: 90px;">
                                                <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.5px; color: #34d399; font-weight: 500;">Confidence</div>
                                                <div style="font-size: 1.15rem; font-weight: 700; color: #10b981;">{confidence:.0f}%</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                st.markdown("---")
                        else:
                            st.warning(
                                f"No recommendations found with predicted rating >= {min_predicted_rating}. "
                                "Try lowering the minimum rating."
                            )
                    else:
                        st.info(
                            f"Could not generate recommendations for User {user_id}. "
                            "This user might be new or not in the training data. "
                            "Try a different User ID."
                        )
            
            except ValueError:
                st.error("Invalid input! Please enter a valid integer User ID.")
            except Exception as e:
                st.error(f"Error generating recommendations: {str(e)}")
    
    # Example Users
    st.markdown("---")
    st.markdown("### 🧪 Try These Example User IDs")
    
    example_users = [1, 42, 100, 500, 1000]
    cols = st.columns(5)
    
    for idx, user_example in enumerate(example_users):
        with cols[idx]:
            if st.button(f"User {user_example}", width="stretch", key=f"example_{user_example}"):
                st.session_state.selected_user = user_example
                st.rerun()
    
    # User Statistics Section
    st.markdown("---")
    st.markdown("### 📊 Dataset Statistics")
    
    try:
        if not ratings_sample.empty:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Sample Users", ratings_sample['userid'].nunique())
            with col2:
                st.metric("Sample Ratings", len(ratings_sample))
            with col3:
                st.metric("Avg Rating", f"{ratings_sample['rating'].mean():.2f}")
            with col4:
                st.metric("Rating Range", f"{ratings_sample['rating'].min()}-{ratings_sample['rating'].max()}")
    except Exception as e:
        st.warning(f"Could not load statistics: {str(e)}")
    
    # Algorithm explanation
    st.markdown("---")
    st.markdown("""
    ### 📌 How This Works
    
    **Collaborative Filtering with SVD:**
    1. Builds a user-movie rating matrix
    2. Uses Singular Value Decomposition (SVD) to reduce dimensions
    3. Finds latent factors representing user preferences
    4. Predicts unknown ratings for new movies
    5. Recommends movies with highest predicted ratings
    
    **Algorithm Details:**
    - **Matrix Factorization**: Decomposes rating matrix into user and movie factors
    - **Latent Factors**: Hidden features capturing user preferences
    - **Rating Prediction**: Dot product of user and movie factors
    - **Recommendation**: Top-k movies with highest predicted ratings
    
    **Advantages:**
    - Captures complex user preferences
    - Discovers hidden patterns in ratings
    - Works across all genres
    - Scalable to large datasets
    
    **Challenges:**
    - Requires user rating history (cold-start for new users)
    - Dense computation for large matrices
    - Can be biased toward popular items
    
    **Use Cases:**
    - Netflix-style personalized recommendations
    - Predicting movie preferences
    - Discovering your next favorite movie
    """)
    
    # User ID Discovery Tips
    st.markdown("---")
    st.markdown("""
    ### 💡 About User IDs
    
    **Where to find User IDs:**
    - Generated during MovieLens user registration
    - Range from 1 to several hundred thousand
    - Each user has a unique ID for tracking preferences
    
    **Tips:**
    - Start with small numbers (1-100) for testing
    - Your personal user ID would be in your MovieLens account
    - The algorithm handles new user IDs gracefully
    """)
