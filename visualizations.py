"""
Visualization and Analytics Module
Creates charts and visualizations for the Streamlit app
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from typing import Dict

PROJECT_ROOT = Path(__file__).resolve().parent
VIZ_PATH = PROJECT_ROOT / "5.visualizations"

# Create visualizations folder if it doesn't exist
VIZ_PATH.mkdir(exist_ok=True)

class MovieVisualizations:
    """Class to handle all visualizations"""
    
    @staticmethod
    @st.cache_data(ttl=3600)
    def rating_distribution(ratings_df: pd.DataFrame) -> go.Figure:
        """Create rating distribution histogram"""
        if ratings_df.empty:
            return go.Figure()
        
        fig = px.histogram(
            ratings_df.sample(n=min(10000, len(ratings_df))),
            x='rating',
            nbins=20,
            title='Rating Distribution',
            labels={'rating': 'Rating', 'count': 'Number of Ratings'},
            color_discrete_sequence=['#667eea']
        )
        fig.update_layout(
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        return fig
    
    @staticmethod
    @st.cache_data(ttl=3600)
    def top_genres(movies_df: pd.DataFrame, n: int = 15) -> go.Figure:
        """Create top genres bar chart"""
        if movies_df.empty:
            return go.Figure()
        
        # Parse genres (assuming pipe-separated)
        genre_list = []
        if 'genres' not in movies_df.columns:
            return go.Figure()

        for genres in movies_df['genres'].dropna():
            if isinstance(genres, str):
                cleaned = [
                    g.strip()
                    for g in genres.split('|')
                    if g.strip().lower() not in ["unknown", "(no genres listed)"]
                ]
                genre_list.extend(cleaned)
        
        genre_counts = pd.Series(genre_list).value_counts().head(n)
        
        fig = px.bar(
            x=genre_counts.values,
            y=genre_counts.index,
            orientation='h',
            title=f'Top {n} Genres',
            labels={'x': 'Count', 'y': 'Genre'},
            color=genre_counts.values,
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            hovermode='y unified',
            template='plotly_white',
            height=400
        )
        return fig
    
    @staticmethod
    @st.cache_data(ttl=3600)
    def release_year_trends(movies_df: pd.DataFrame) -> go.Figure:
        """Create movies release by year line chart"""
        if movies_df.empty:
            return go.Figure()
        
        if 'release_year' not in movies_df.columns:
            return go.Figure()

        valid_movies = movies_df[
            (movies_df["release_year"].notna()) &
            (movies_df["release_year"] > 0)
        ]

        year_counts = valid_movies["release_year"].value_counts().sort_index()
        
        fig = px.line(
            x=year_counts.index,
            y=year_counts.values,
            title='Movies Released by Year',
            labels={'x': 'Year', 'y': 'Number of Movies'},
            markers=True,
            color_discrete_sequence=['#764ba2']
        )
        fig.update_layout(
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        return fig
    
    @staticmethod
    @st.cache_data(ttl=3600)
    def top_rated_movies(movies_df: pd.DataFrame, ratings_df: pd.DataFrame, 
                        n: int = 10, min_ratings: int = 100) -> go.Figure:
        """Create top rated movies bar chart"""
        if ratings_df.empty or movies_df.empty:
            return go.Figure()
        
        # Calculate movie ratings
        required_cols = ['movieid', 'rating']

        if not all(col in ratings_df.columns for col in required_cols):
            return go.Figure()

        movie_stats = ratings_df.groupby('movieid').agg({
        'rating': ['mean', 'count']
        }).reset_index()
        movie_stats.columns = ['movieid', 'avg_rating', 'rating_count']
        movie_stats = movie_stats[movie_stats['rating_count'] >= min_ratings]
        movie_stats = movie_stats.nlargest(n, 'avg_rating')
        
        # Merge with movie names
        movie_stats = movie_stats.merge(
            movies_df[['movieid', 'title']],
            on='movieid',
            how='left'
        )

        movie_stats = movie_stats.dropna(subset=["title"])
        
        fig = px.bar(
            movie_stats,
            x='avg_rating',
            y='title',
            orientation='h',
            title=f'Top {n} Highest Rated Movies',
            labels={'avg_rating': 'Average Rating', 'title': 'Movie'},
            color='avg_rating',
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(
            hovermode='y unified',
            template='plotly_white',
            height=400
        )
        return fig
    
    @staticmethod
    @st.cache_data(ttl=3600)
    def recommendations_by_type(popularity_df: pd.DataFrame) -> go.Figure:
        """Create pie chart of recommendation types"""
        recommendation_counts = {
            'Popularity-Based': len(popularity_df),
            'Content-Based': 1,
            'Collaborative Filtering': 1
        }
        
        fig = px.pie(
            names=recommendation_counts.keys(),
            values=recommendation_counts.values(),
            title='Recommendation System Coverage',
            color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1']
        )
        fig.update_layout(template='plotly_white', height=400)
        return fig
    
    @staticmethod
    @st.cache_data(ttl=3600)
    def movies_per_year_box(movies_df: pd.DataFrame, 
                           ratings_df: pd.DataFrame) -> go.Figure:
        """Create box plot of ratings per year"""
        if ratings_df.empty or movies_df.empty:
            return go.Figure()
         
        sample_ratings = ratings_df.sample(
            n=min(50000, len(ratings_df)),
            random_state=42
        )

        merged = sample_ratings.merge(
            movies_df[['movieid', 'release_year']],
            on='movieid'
        )

        merged = merged[
            (merged["release_year"].notna()) &
            (merged["release_year"] > 0)
        ]
        
        # Group by decade
        merged['decade'] = (merged['release_year'] // 10 * 10).astype(str) + 's'
        
        fig = px.box(
            merged,
            x='decade',
            y='rating',
            title='Rating Distribution by Decade',
            labels={'decade': 'Decade', 'rating': 'Rating'},
            color_discrete_sequence=['#667eea']
        )
        fig.update_layout(
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        return fig
    
    @staticmethod
    def save_all_visualizations(movies_df: pd.DataFrame, 
                               ratings_df: pd.DataFrame,
                               popularity_df: pd.DataFrame) -> Dict:
        """Generate and save all visualizations"""
        try:
            saved_files = {}
            
            # Create figures
            figures = {
                'rating_distribution': MovieVisualizations.rating_distribution(ratings_df),
                'top_genres': MovieVisualizations.top_genres(movies_df),
                'release_trends': MovieVisualizations.release_year_trends(movies_df),
                'top_rated': MovieVisualizations.top_rated_movies(movies_df, ratings_df),
                'recommendations': MovieVisualizations.recommendations_by_type(popularity_df),
                'ratings_by_decade': MovieVisualizations.movies_per_year_box(movies_df, ratings_df)
            }
            
            # Save as HTML
            for name, fig in figures.items():
                if fig and len(fig.data) > 0:
                    filepath = VIZ_PATH / f"{name}.html"
                    fig.write_html(str(filepath))
                    saved_files[name] = str(filepath)
            
            return saved_files
        except Exception as e:
            st.error(f"Error saving visualizations: {str(e)}")
            return {}


class DashboardMetrics:
    """Display key metrics on dashboard"""
    
    @staticmethod
    def display_metrics(stats: Dict) -> None:
        """Display key metrics in columns"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="📽️ Total Movies",
                value=f"{stats.get('total_movies', 0):,}",
                delta="Movies in Database"
            )
        
        with col2:
            st.metric(
                label="⭐ Total Ratings",
                value=f"{stats.get('total_ratings', 0):,}",
                delta="User Ratings"
            )
        
        with col3:
            st.metric(
                label="👥 Unique Users",
                value=f"{stats.get('unique_users', 0):,}",
                delta="Rated Movies"
            )
        
        col4, col5, col6 = st.columns(3)
        
        with col4:
            st.metric(
                label="🎭 Genres",
                value=f"{stats.get('genres_count', 0):,}",
                delta="Movie Categories"
            )
        
        with col5:
            st.metric(
                label="📊 Popular Movies",
                value=f"{stats.get('top_movies', 0):,}",
                delta="In Recommendation List"
            )
        
        with col6:
            st.metric(
                label="📅 Years Covered",
                value=stats.get('release_years', 'N/A'),
                delta="Release Year Range"
            )


class RecommendationDisplay:
    """Display recommendations in attractive cards"""
    
    @staticmethod
    def display_movie_card(movie_info: Dict, card_type: str = 'info') -> None:
        """Display a single movie as a card"""
        genres = movie_info.get('genres', 'N/A')
        year = movie_info.get('release_year', 'N/A')
        
        score = None
        if card_type == 'content_based':
            score = movie_info.get('similarity_score', 0)
            score_label = "Similarity Score"
        elif card_type == 'collaborative':
            score = movie_info.get('predicted_rating', 0)
            score_label = "Predicted Rating"
        else:
            score = movie_info.get('avg_rating', 0)
            score_label = "Average Rating"
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### 🎬 {movie_info.get('title', 'Unknown')}")
            st.write(f"**Genres:** {genres}")
            st.write(f"**Year:** {year}")
        
        with col2:
            if score is not None:
                st.metric(score_label, f"{score:.2f}")
    
    @staticmethod
    def display_recommendations(recommendations_df: pd.DataFrame, 
                               card_type: str = 'info') -> None:
        """Display all recommendations"""
        if recommendations_df.empty:
            st.warning("No recommendations found.")
            return
        
        for idx, row in recommendations_df.iterrows():
            RecommendationDisplay.display_movie_card(
                row.to_dict(),
                card_type=card_type
            )
            st.markdown("---")
