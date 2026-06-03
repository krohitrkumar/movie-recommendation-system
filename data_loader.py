"""
Data Loading and Caching Module
Handles efficient loading of CSV files and models with Streamlit caching
"""

import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
from typing import Dict, Optional

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parent
# CSV LOADERS
@st.cache_data(ttl=3600)
def load_movies_data() -> pd.DataFrame:
    try:
        path = PROJECT_ROOT / "3.outputs" / "movies_processed.csv"
        return pd.read_csv(path)

    except Exception as e:
        st.error(f"Error loading movies data: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def load_popularity_recommendations() -> pd.DataFrame:
    try:
        path = PROJECT_ROOT / "3.outputs" / "popularity_based_recommendation.csv"
        return pd.read_csv(path)

    except Exception as e:
        st.error(f"Error loading popularity recommendations: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def load_ratings_data(sample: Optional[int] = None) -> pd.DataFrame:
    try:
        path = PROJECT_ROOT / "3.outputs" / "ratings_processed.csv"

        df = pd.read_csv(path)

        if sample:
            df = df.sample(
                n=min(sample, len(df)),
                random_state=42
            )

        return df

    except Exception as e:
        st.error(f"Error loading ratings data: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def load_tags_data(sample: Optional[int] = None) -> pd.DataFrame:
    try:
        path = PROJECT_ROOT / "3.outputs" / "tags_processed.csv"

        df = pd.read_csv(path)

        if sample:
            df = df.sample(
                n=min(sample, len(df)),
                random_state=42
            )

        return df

    except Exception as e:
        st.error(f"Error loading tags data: {e}")
        return pd.DataFrame()



# MODEL LOADERS

@st.cache_resource
def load_content_recommender():
    try:
        path = PROJECT_ROOT / "4.models" / "movie_content_recommender.pkl"

        model = joblib.load(path)

        return model

    except Exception as e:
        st.error(f"Error loading content recommender model: {e}")
        return None


@st.cache_resource
def load_collaborative_filtering_model():
    try:
        path = PROJECT_ROOT / "4.models" / "collaborative_filtering_svd.pkl"

        model = joblib.load(path)

        return model

    except Exception as e:
        st.error(f"Error loading collaborative filtering model: {e}")
        return None


# FILE CHECKER


def verify_project_files() -> Dict[str, bool]:

    return {
        "movies_processed.csv":
            (PROJECT_ROOT / "3.outputs" / "movies_processed.csv").exists(),

        "ratings_processed.csv":
            (PROJECT_ROOT / "3.outputs" / "ratings_processed.csv").exists(),

        "tags_processed.csv":
            (PROJECT_ROOT / "3.outputs" / "tags_processed.csv").exists(),

        "popularity_based_recommendation.csv":
            (PROJECT_ROOT / "3.outputs" / "popularity_based_recommendation.csv").exists(),

        "movie_content_recommender.pkl":
            (PROJECT_ROOT / "4.models" / "movie_content_recommender.pkl").exists(),

        "collaborative_filtering_svd.pkl":
            (PROJECT_ROOT / "4.models" / "collaborative_filtering_svd.pkl").exists(),
    }


def get_project_stats() -> Dict:

    try:

        movies = load_movies_data()
        ratings = load_ratings_data()
        popularity = load_popularity_recommendations()
        valid_years = movies.loc[movies["release_year"] > 0, "release_year"]
        stats = {
            "total_movies":
                len(movies),

            "total_ratings":
                len(ratings),

            "unique_users":
                ratings["userid"].nunique()
                if not ratings.empty and "userid" in ratings.columns
                else 0,

            "top_movies":
                len(popularity),

            "genres_count":
                movies["genres"].nunique()
                if not movies.empty and "genres" in movies.columns
                else 0,

            

            "release_years":
                f"{valid_years.min()} - {valid_years.max()}"
                if not valid_years.empty
                else "N/A"
        }

        return stats

    except Exception as e:
        st.error(f"Error getting project stats: {e}")
        return {}