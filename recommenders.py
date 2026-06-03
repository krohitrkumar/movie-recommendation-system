"""
Recommendation Engine Module
Handles all three types of recommendations with proper error handling
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
from difflib import SequenceMatcher
import re

class MovieSearchEngine:
    """Fuzzy search engine for movies with autocomplete"""
    
    def __init__(self, movies_df: pd.DataFrame):
        self.movies_df = movies_df
        self.movie_titles = movies_df['title'].unique().tolist()
    
    def fuzzy_search(self, query: str, threshold: float = 0.6) -> List[str]:
        """Fuzzy match for movie titles"""
        matches = []
        query_lower = query.lower()
        
        for title in self.movie_titles:
            ratio = SequenceMatcher(None, query_lower, title.lower()).ratio()
            if ratio >= threshold:
                matches.append((title, ratio))
        
        # Sort by similarity score
        matches.sort(key=lambda x: x[1], reverse=True)
        return [title for title, _ in matches[:10]]
    
    def partial_match(self, query: str) -> List[str]:
        """Partial string matching"""
        query_lower = query.lower()
        matches = [title for title in self.movie_titles if query_lower in title.lower()]
        return matches[:10]
    
    def search(self, query: str) -> Tuple[Optional[pd.Series], List[str]]:
        """Search for a movie and return exact match or suggestions"""
        if not query.strip():
            return None, []
        
        # Try exact match (case-insensitive)
        query_lower = query.lower()
        exact = self.movies_df[self.movies_df['title'].str.lower() == query_lower]
        
        if not exact.empty:
            return exact.iloc[0], []
        
        # Try fuzzy and partial matches
        fuzzy_results = self.fuzzy_search(query)
        partial_results = self.partial_match(query)
        
        # Combine and deduplicate suggestions
        suggestions = list(dict.fromkeys(fuzzy_results + partial_results))
        
        return None, suggestions


class PopularityRecommender:
    """Popularity-based recommendation engine"""
    
    def __init__(self, popularity_df: pd.DataFrame, movies_df: pd.DataFrame):
        self.popularity_df = popularity_df.copy()
        self.movies_df = movies_df
        self._prepare_data()
    
    def _prepare_data(self):
        """Merge popularity data with movie metadata"""
        try:
            self.recommendations = self.popularity_df.merge(
                self.movies_df[['title', 'genres', 'release_year']],
                on='title',
                how='left'
            )
        except Exception as e:
            st.error(f"Error preparing popularity data: {str(e)}")
            self.recommendations = self.popularity_df.copy()
    
    def get_top_movies(self, n: int = 10) -> pd.DataFrame:
        """Get top N popular movies"""
        return self.recommendations.head(n).copy()
    
    def get_movies_by_count(self, min_ratings: int = 100) -> pd.DataFrame:
        """Get movies with minimum rating count"""
        return self.recommendations[
            self.recommendations['rating_count'] >= min_ratings
        ].head(20).copy()


class ContentBasedRecommender:
    """Content-based recommendation engine"""
    
    def __init__(self, model, movies_df: pd.DataFrame):
        self.model = model
        self.movies_df = movies_df
        
        # Create movie index mapping if available
        self.indices = model.get("indices")
        self.movies_content = model.get("movies_content")
        self.tfidf_matrix = model.get("tfidf_matrix")
        
        if self.indices is None:
            raise ValueError("indices not found in model")

        if self.movies_content is None:
            raise ValueError("movies_content not found in model")

        if self.tfidf_matrix is None:
            raise ValueError("tfidf_matrix not found in model")

        # Remove duplicate titles
        if hasattr(self.indices, "index"):
            self.indices = self.indices[~self.indices.index.duplicated(keep="first")]
    
    def get_recommendations(self, movie_title: str, n: int = 10) -> pd.DataFrame:

        try:

            if movie_title not in self.indices.index:
                return pd.DataFrame()

            movie_idx = int(self.indices.loc[movie_title])

            from sklearn.metrics.pairwise import cosine_similarity

            similarity_scores = cosine_similarity(
                self.tfidf_matrix[movie_idx],
                self.tfidf_matrix
            ).flatten()

            movie_indices = similarity_scores.argsort()[::-1][1:n+1]

            recommendations = self.movies_content.iloc[
                movie_indices
            ][['title', 'genres']].copy()

            recommendations['similarity_score'] = (
                similarity_scores[movie_indices]
            )

            return recommendations

        except Exception as e:
            st.error(f"Error getting recommendations: {e}")
            return pd.DataFrame()
                               
        
class CollaborativeFilteringRecommender:
    """Collaborative filtering recommendation engine"""
    
    def __init__(self, model, movies_df: pd.DataFrame):
        self.model = model
        self.movies_df = movies_df
        
        # Extract user and movie mappings from model
        if hasattr(model, 'trainset'):
            self.trainset = model.trainset
            self.ur = model.trainset.ur
            self.ir = model.trainset.ir
        else:
            self.ur = {}
            self.ir = {}
    
    def get_recommendations(self, user_id: int, n: int = 10) -> pd.DataFrame:
        """Get collaborative filtering recommendations for a user"""
        try:
            # Get movies the user has rated
            rated_movies = set()
            if hasattr(self.model, 'trainset'):
                if user_id in self.ur:
                    rated_movies = {self.model.trainset.to_raw_iid(iid) 
                                  for iid, _ in self.ur[user_id]}
            
            # Predict ratings for movies
            all_movies = self.movies_df[['movieid', 'title']]
            predictions = []

            for _, row in all_movies.iterrows():

                movie_id = row['movieid']
                movie_title = row['title']

                if movie_id not in rated_movies:

                    try:
                        pred = self.model.predict(user_id, movie_id)

                        predictions.append({
                            'title': movie_title,
                            'predicted_rating': pred.est
                        })

                    except:
                        continue
            
            if not predictions:
                return pd.DataFrame()
            
            # Sort by predicted rating
            predictions_df = pd.DataFrame(predictions)
            recommendations = predictions_df.nlargest(n, 'predicted_rating')
            
            # Merge with movie details
            recommendations = recommendations.merge(
                self.movies_df[['title', 'genres', 'release_year']],
                on='title',
                how='left'
            )
            
            return recommendations
            
        except Exception as e:
            st.error(f"Error getting collaborative filtering recommendations: {str(e)}")
            return pd.DataFrame()
    
    def get_user_stats(self, user_id: int) -> Dict:
        """Get statistics about user's rating behavior"""
        try:
            if hasattr(self.model, 'trainset') and user_id in self.ur:
                ratings = [rating for _, rating in self.ur[user_id]]
                return {
                    'rated_movies': len(ratings),
                    'avg_rating': np.mean(ratings),
                    'min_rating': np.min(ratings),
                    'max_rating': np.max(ratings)
                }
            return {}
        except Exception as e:
            st.error(f"Error getting user stats: {str(e)}")
            return {}


def create_movie_search_engine(movies_df: pd.DataFrame) -> MovieSearchEngine:
    """Factory function to create movie search engine"""
    return MovieSearchEngine(movies_df)

def create_popularity_recommender(popularity_df: pd.DataFrame, 
                                 movies_df: pd.DataFrame) -> PopularityRecommender:
    """Factory function to create popularity recommender"""
    return PopularityRecommender(popularity_df, movies_df)

def create_content_recommender(model, movies_df: pd.DataFrame) -> ContentBasedRecommender:
    """Factory function to create content recommender"""
    return ContentBasedRecommender(model, movies_df)

def create_collaborative_recommender(model, movies_df: pd.DataFrame) -> CollaborativeFilteringRecommender:
    """Factory function to create collaborative filtering recommender"""
    return CollaborativeFilteringRecommender(model, movies_df)
