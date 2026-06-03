"""
Popularity-Based Recommendations Page
Display top-rated and most popular movies
"""

import streamlit as st
import pandas as pd
from data_loader import load_popularity_recommendations, load_movies_data
from recommenders import create_popularity_recommender
from visualizations import RecommendationDisplay

def show_popularity():
    """Display popularity-based recommendations"""
    
    st.markdown("## 📊 Popularity-Based Recommendations")
    st.markdown("""
    These recommendations are based on **overall ratings and popularity** across all users.
    Great for discovering well-received movies!
    """)
    
    # Load data
    with st.spinner("Loading data..."):
        movies_df = load_movies_data()
        popularity_df = load_popularity_recommendations()
    
    if popularity_df.empty:
        st.error("Could not load popularity recommendations. Please check data files.")
        return
    
    # Create recommender
    recommender = create_popularity_recommender(popularity_df, movies_df)
    
    # Sidebar controls
    with st.sidebar:
        st.markdown("### ⚙️ Recommendation Settings")
        n_recommendations = st.slider(
            "Number of Recommendations",
            min_value=5,
            max_value=50,
            value=10,
            step=5
        )
        
        min_ratings = st.slider(
            "Minimum Ratings Count",
            min_value=10,
            max_value=1000,
            value=100,
            step=50
        )
    
    # Tab layout
    tab1, tab2, tab3 = st.tabs(["🏆 Top Movies", "📈 Statistics", "📊 Metrics"])
    
    with tab1:
        st.markdown("### Top Popular Movies")
        
        # Get top movies
        top_movies = recommender.get_top_movies(n=n_recommendations)
        
        if not top_movies.empty:
            # Display in cards
            for idx, row in top_movies.iterrows():
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"### 🎬 {row['title']}")
                    if pd.notna(row.get('genres')):
                        st.write(f"**Genres:** {row['genres']}")
                    if pd.notna(row.get('release_year')):
                        st.write(f"**Year:** {int(row['release_year'])}")
                
                with col2:
                    st.metric(
                        "Average Rating",
                        f"{row['avg_rating']:.2f}/5.0"
                    )
                
                with col3:
                    st.metric(
                        "Ratings Count",
                        f"{int(row['rating_count']):,}"
                    )
                
                st.markdown("---")
        else:
            st.warning("No recommendations available.")
    
    with tab2:
        st.markdown("### Popularity Statistics")
        
        # Get movies with minimum rating count
        popular_by_count = recommender.get_movies_by_count(min_ratings=min_ratings)
        
        if not popular_by_count.empty:
            st.markdown(f"**Movies with {min_ratings}+ ratings:**")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Total Movies",
                    len(popular_by_count)
                )
            
            with col2:
                st.metric(
                    "Avg Rating",
                    f"{popular_by_count['avg_rating'].mean():.2f}"
                )
            
            with col3:
                st.metric(
                    "Max Rating",
                    f"{popular_by_count['avg_rating'].max():.2f}"
                )
            
            with col4:
                st.metric(
                    "Min Rating",
                    f"{popular_by_count['avg_rating'].min():.2f}"
                )
            
            st.markdown("---")
            st.markdown("### Popular Movies Table")
            
            display_df = popular_by_count[[
                'title', 'avg_rating', 'rating_count', 'genres'
            ]].copy()
            display_df.columns = ['Movie Title', 'Avg Rating', 'Ratings', 'Genres']
            display_df = display_df.sort_values('Avg Rating', ascending=False)
            
            st.dataframe(display_df, width="stretch", height=400)
        else:
            st.warning(f"No movies found with {min_ratings}+ ratings.")
    
    with tab3:
        st.markdown("### Rating Distribution Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Recommendation Statistics")
            stats = {
                'Total Recommendations': len(popularity_df),
                'Avg Rating': f"{popularity_df['avg_rating'].mean():.2f}",
                'Median Rating': f"{popularity_df['avg_rating'].median():.2f}",
                'Std Dev': f"{popularity_df['avg_rating'].std():.2f}",
                'Min Rating': f"{popularity_df['avg_rating'].min():.2f}",
                'Max Rating': f"{popularity_df['avg_rating'].max():.2f}",
            }
            
            for key, value in stats.items():
                st.write(f"**{key}:** {value}")
        
        with col2:
            st.markdown("#### Rating Count Statistics")
            stats2 = {
                'Avg Rating Count': f"{popularity_df['rating_count'].mean():.0f}",
                'Median Rating Count': f"{popularity_df['rating_count'].median():.0f}",
                'Min Rating Count': f"{popularity_df['rating_count'].min():.0f}",
                'Max Rating Count': f"{popularity_df['rating_count'].max():.0f}",
                'Total Ratings': f"{popularity_df['rating_count'].sum():.0f}",
            }
            
            for key, value in stats2.items():
                st.write(f"**{key}:** {value}")
        
        # Visualizations
        st.markdown("---")
        st.markdown("#### Rating Distribution Histogram")
        
        fig = st.empty()
        
        try:
            import plotly.express as px
            
            hist_fig = px.histogram(
                popularity_df,
                x='avg_rating',
                nbins=20,
                title='Distribution of Average Ratings',
                labels={'avg_rating': 'Average Rating', 'count': 'Number of Movies'},
                color_discrete_sequence=['#667eea']
            )
            hist_fig.update_layout(
                template='plotly_white',
                height=400,
                hovermode='x unified'
            )
            st.plotly_chart(hist_fig, width="stretch")
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
    
    # Additional Info
    st.markdown("---")
    st.markdown("""
    ### 📌 How This Works
    
    **Popularity-Based Recommendations:**
    1. Calculates average rating for each movie
    2. Counts the number of ratings received
    3. Ranks movies by rating + popularity
    4. Displays top-rated and well-reviewed movies
    
    **Advantages:**
    - Works for new users (no history needed)
    - Discovers trending movies
    - Highlights quality content
    - Simple and interpretable
    
    **Use Cases:**
    - Finding blockbuster movies
    - Discovering critically acclaimed films
    - Getting baseline recommendations for new users
    """)
