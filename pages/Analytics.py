"""
Analytics and Visualizations Page
Comprehensive data analysis and visualizations
"""

import streamlit as st
import pandas as pd
import numpy as np
from data_loader import load_movies_data, load_ratings_data, load_popularity_recommendations
from visualizations import MovieVisualizations, DashboardMetrics
from pathlib import Path
def show_analytics():
    """Display analytics and visualizations"""
    
    st.markdown("## 📈 Analytics & Visualizations")
    st.markdown("""
    Comprehensive analysis and visualizations of the movie dataset and recommendation system.
    """)
    
    # Load data
    with st.spinner("Loading data for analysis..."):
        movies_df = load_movies_data()
        ratings_sample = load_ratings_data(sample=100000)
        popularity_df = load_popularity_recommendations()
    
    if movies_df.empty:
        st.error("Could not load movie data.")
        return
    
    # Tabs for different analyses
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard",
        "🎬 Movie Analysis",
        "⭐ Rating Analysis",
        "📉 Trends",
        "💾 Export"
    ])
    
    with tab1:
        st.markdown("### 📊 Key Metrics Dashboard")
        valid_years = movies_df.loc[movies_df["release_year"] > 0, "release_year"]

        stats = {
            'total_movies': len(movies_df),
            'total_ratings': len(ratings_sample) if not ratings_sample.empty else 0,
            'unique_users': ratings_sample['userid'].nunique() if not ratings_sample.empty else 0,
            'top_movies': len(popularity_df),
            'genres_count': movies_df['genres'].nunique(),
            'release_years': f"{valid_years.min()}-{valid_years.max()}",
        }
        
        DashboardMetrics.display_metrics(stats)
        
        st.markdown("---")
        st.markdown("### 📋 Sample Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Top 10 Movies")
            top_10 = popularity_df.head(10)[['title', 'avg_rating', 'rating_count']]
            st.dataframe(top_10, use_container_width=True)
        
        with col2:
            st.markdown("#### Latest Movies (by year)")
            latest = (
                movies_df[movies_df["release_year"] > 0]
                .nlargest(10, "release_year")
                [["title", "release_year", "genres"]]
            )
            st.dataframe(latest, use_container_width=True)
    
    with tab2:
        st.markdown("### 🎬 Movie Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Top Genres Distribution")
            clean_movies = movies_df.copy()

            clean_movies = clean_movies[
                ~clean_movies["genres"]
                .fillna("")
                .str.contains("unknown", case=False)
            ]

            clean_movies = clean_movies[
                ~clean_movies["genres"]
                .fillna("")
                .str.contains(r"\(no genres listed\)", case=False)
            ]
            try:
                genre_fig = MovieVisualizations.top_genres(movies_df, n=15)
                st.plotly_chart(genre_fig, width="stretch")
            except Exception as e:
                st.error(f"Error creating genres chart: {str(e)}")
        
        with col2:
            st.markdown("#### Movies Released by Year")
            try:
                year_fig = MovieVisualizations.release_year_trends(movies_df)
                st.plotly_chart(year_fig, width="stretch")
            except Exception as e:
                st.error(f"Error creating year trends chart: {str(e)}")
        
        st.markdown("---")
        st.markdown("#### Release Year Statistics")
        
        valid_movies = movies_df[movies_df["release_year"] > 0]

        year_stats = {
            'Earliest Movie': int(valid_movies['release_year'].min()),
            'Latest Movie': int(valid_movies['release_year'].max()),
            'Average Year': f"{valid_movies['release_year'].mean():.0f}",
            'Most Movies in Year': valid_movies['release_year'].value_counts().idxmax(),
            'Total Years Covered': int(
                valid_movies['release_year'].max()
                - valid_movies['release_year'].min()
                + 1
            ),
        }
        col1, col2, col3, col4, col5 = st.columns(5)
        metrics = list(year_stats.items())
        
        cols = [col1, col2, col3, col4, col5]
        for (label, value), col in zip(metrics, cols):
            with col:
                st.metric(label, value)
    
    with tab3:
        st.markdown("### ⭐ Rating Analysis")
        
        if not ratings_sample.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Rating Distribution")
                try:
                    rating_fig = MovieVisualizations.rating_distribution(ratings_sample)
                    st.plotly_chart(rating_fig, width="stretch")
                except Exception as e:
                    st.error(f"Error creating rating distribution: {str(e)}")
            
            with col2:
                st.markdown("#### Top Rated Movies")
                try:
                    top_rated_fig = MovieVisualizations.top_rated_movies(
                        movies_df,
                        ratings_sample,
                        n=10,
                        min_ratings=100
                    )
                    st.plotly_chart(top_rated_fig, width="stretch")
                except Exception as e:
                    st.error(f"Error creating top rated chart: {str(e)}")
            
            st.markdown("---")
            st.markdown("#### Rating Statistics")
            
            rating_stats = {
                'Total Ratings': len(ratings_sample),
                'Average Rating': f"{ratings_sample['rating'].mean():.2f}",
                'Median Rating': f"{ratings_sample['rating'].median():.2f}",
                'Std Deviation': f"{ratings_sample['rating'].std():.2f}",
                'Min Rating': f"{ratings_sample['rating'].min():.1f}",
                'Max Rating': f"{ratings_sample['rating'].max():.1f}",
            }
            
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            metrics = list(rating_stats.items())
            
            cols = [col1, col2, col3, col4, col5, col6]
            for (label, value), col in zip(metrics, cols):
                with col:
                    st.metric(label, value)
        else:
            st.warning("Rating data not available for analysis.")
    
    with tab4:
        st.markdown("### 📉 Trend Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Ratings by Decade")
            try:
                decade_fig = MovieVisualizations.movies_per_year_box(
                    movies_df,
                    ratings_sample
                )
                st.plotly_chart(decade_fig, width="stretch")
            except Exception as e:
                st.error(f"Error creating decade analysis: {str(e)}")
        
        with col2:
            st.markdown("#### Recommendation Coverage")
            try:
                rec_fig = MovieVisualizations.recommendations_by_type(popularity_df)
                st.plotly_chart(rec_fig, width="stretch")
            except Exception as e:
                st.error(f"Error creating recommendation chart: {str(e)}")
    
    with tab5:
        st.markdown("### 💾 Export & Visualizations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Export Datasets")
            
            # Export movies
            if st.button("📥 Download Movies Data", key="download_movies"):
                csv_movies = movies_df.to_csv(index=False)

                st.download_button(
                    "📥 Download Movies Data",
                    csv_movies,
                    file_name="movies_processed.csv",
                    mime="text/csv"
                )
            
            # Export popularity
            if st.button("📥 Download Popularity Rankings", key="download_popularity"):
                csv = popularity_df.to_csv(index=False)
                st.download_button(
                    label="📁 popularity_based_recommendation.csv",
                    data=csv,
                    file_name="popularity_based_recommendation.csv",
                    mime="text/csv"
                )
        
        with col2:
            st.markdown("#### Save Visualizations")
            
            if st.button("💾 Generate All Visualizations"):
                with st.spinner("Generating visualizations..."):
                    try:
                        saved = MovieVisualizations.save_all_visualizations(
                            movies_df,
                            ratings_sample,
                            popularity_df
                        )
                        
                        if saved:
                            st.success("✅ Visualizations generated successfully!")
                            st.info(f"Saved {len(saved)} visualizations to 5.visualizations/")
                            
                            for name, path in saved.items():
                                st.write(f"- {name}.html")
                        else:
                            st.warning("No visualizations were generated.")
                    except Exception as e:
                        st.error(f"Error generating visualizations: {str(e)}")
        
        st.markdown("---")
        st.markdown("#### 📊 Visualization Files")
    
        viz_path = Path(__file__).resolve().parent.parent / "5.visualizations"

        if not viz_path.exists():
            viz_path.mkdir(parents=True, exist_ok=True)

        viz_files = sorted(viz_path.glob("*.html"))

        if viz_files:
            st.success(f"Found {len(viz_files)} saved visualizations:")

            for file in viz_files:
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.write(f"📊 {file.name}")

                with col2:
                    if st.button("👁️ View", key=f"view_{file.stem}"):

                        html_content = file.read_text(encoding="utf-8")

                        st.code(
                            html_content[:2000],
                            language="html"
                        )
    
    # Statistics Summary
    st.markdown("---")
    st.markdown("""
    ### 📌 About This Analysis
    
    **Dataset Overview:**
    - Movies processed and cleaned from MovieLens
    - User ratings spanning multiple decades
    - Comprehensive genre classification
    - Complete movie metadata
    
    **Analysis Features:**
    - Distribution analysis of ratings
    - Genre popularity trends
    - Release year statistics
    - Top-rated movies by user consensus
    - Rating patterns across time periods
    
    **Visualizations:**
    - Interactive Plotly charts
    - Exportable HTML versions
    - Drill-down capability
    - Hover details and statistics
    """)
