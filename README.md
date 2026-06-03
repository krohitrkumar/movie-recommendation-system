# 🎥 Smart Movie Recommender

An end-to-end Movie Recommendation System built using Machine Learning, SQL, PostgreSQL, and Streamlit.

Smart Movie Recommender combines multiple recommendation techniques to help users discover movies through popularity rankings, content similarity, and collaborative filtering. The project includes a complete data pipeline starting from raw MovieLens data, database processing, exploratory analysis, model development, and deployment through an interactive Streamlit web application.

---

## 🌐 Live Demo

**Application:** [Open Smart Movie Recommender]([https://smart-movie-recomendation.streamlit.app/])

**GitHub Repository:** https://github.com/krohitrkumar/movie-recommendation-system

---

## 📌 Project Overview

This project was developed to explore recommendation systems and understand how large-scale movie recommendation platforms work.

The project covers:

* Database design and SQL querying
* Data cleaning and preprocessing
* Exploratory Data Analysis (EDA)
* Feature engineering
* Machine Learning model development
* Interactive dashboard creation
* Model deployment using Streamlit

The application allows users to:

* Browse top-rated movies
* Discover similar movies
* Receive personalized recommendations
* Explore dataset analytics
* Analyze rating trends and movie patterns

---

## 📊 Dataset

### MovieLens Dataset

Source: GroupLens Research

Dataset Characteristics:

* 83,000+ Movies
* 33,000,000+ Ratings
* 330,000+ Users
* Multiple decades of movie data

### Available Information

#### Movies

* Movie Title
* Release Year
* Genres

#### Ratings

* User ID
* Movie ID
* Rating (0.5 – 5.0)

#### Tags

* User-generated tags
* Movie descriptions

#### Temporal Features

* Rating timestamps
* Historical movie trends

---

## ⚙️ Data Pipeline

### 1. Database Setup

* PostgreSQL database creation
* Schema design
* Index creation
* Table relationships

### 2. Data Loading

* ETL process
* Importing raw CSV files
* Data validation

### 3. Data Validation

* Null value checks
* Duplicate detection
* Data integrity verification

### 4. Data Preparation

* Feature engineering
* Genre processing
* Release year extraction
* Data normalization

### 5. Exploratory Data Analysis

* Rating distributions
* Popular genres
* User activity analysis
* Movie release trends

### 6. Recommendation Modeling

* Popularity-Based Recommendation
* Content-Based Filtering
* Collaborative Filtering

---

## 🧠 Recommendation Approaches

### 1. Popularity-Based Recommendation

#### Method

* Average rating ranking
* Review count weighting
* Statistical popularity scoring

#### Advantages

* Works for new users
* Easy to understand
* Reliable recommendations

#### Limitations

* No personalization
* Favors popular movies

---

### 2. Content-Based Filtering

#### Method

* TF-IDF Vectorization
* Cosine Similarity
* Metadata similarity matching

#### Features Used

* Genres
* Movie metadata
* Text-based attributes

#### Advantages

* No user history required
* Transparent recommendations
* Less popularity bias

#### Limitations

* Limited discovery
* Dependent on available metadata

---

### 3. Collaborative Filtering

#### Method

* SVD Matrix Factorization
* Latent Factor Modeling
* User-Item Interaction Analysis

#### Advantages

* Personalized recommendations
* Learns hidden patterns
* Discovers unexpected movies

#### Limitations

* Cold-start problem
* Requires sufficient rating data

---

## 🛠 Technology Stack

### Programming Language

* Python 3.8+

### Data Analysis

* Pandas
* NumPy

### Machine Learning

* Scikit-Learn
* Surprise

### Visualization

* Plotly
* Plotly Express

### Database

* PostgreSQL
* SQLAlchemy

### Dashboard

* Streamlit
* Custom CSS

### Development

* Jupyter Notebook
* Git

---

## 📂 Project Structure

```text
movie_recommendation_project/
│
├── 0.data/
│   ├── movies.csv
│   ├── ratings.csv
│   ├── tags.csv
│   └── links.csv
│
├── 1.sql/
│   ├── 01_database_setup.sql
│   ├── 02_load_data.sql
│   ├── 03_validation.sql
│   ├── 04_data_preparation.sql
│   └── 05_eda.sql
│
├── 2.notebook/
│   ├── 01_database_connection.ipynb
│   ├── 02_python_preprocessing.ipynb
│   ├── 03_visualization_eda.ipynb
│   └── 04_recommendation_system.ipynb
│
├── 3.outputs/
│   ├── movies_processed.csv
│   ├── ratings_processed.csv
│   ├── tags_processed.csv
│   └── popularity_based_recommendation.csv
│
├── 4.models/
│   ├── movie_content_recommender.pkl
│   └── collaborative_filtering_svd.pkl
│
├── 5.visualizations/
│
├── pages/
│   ├── Home.py
│   ├── Popularity.py
│   ├── Content_Based.py
│   ├── Collaborative_Filtering.py
│   ├── Analytics.py
│   └── About.py
│
├── app.py
├── data_loader.py
├── recommenders.py
├── visualizations.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone <repository-url>
cd movie_recommendation_project
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## 📈 Dashboard Features

### Home

* Project overview
* Dataset statistics
* Quick navigation

### Popularity-Based Recommendations

* Top-rated movies
* Popularity rankings
* Rating statistics

### Content-Based Recommendations

* Similar movie discovery
* Genre-based matching
* Metadata similarity analysis

### Collaborative Filtering

* Personalized recommendations
* User-specific movie suggestions
* SVD prediction engine

### Analytics

* Rating distribution
* Genre analysis
* Movie release trends
* Recommendation coverage
* Interactive visualizations

---

## 💡 Learning Notes

This project was also used to gain hands-on experience with Large Language Models (LLMs) and AI-assisted development tools.

Tools used during development include:

* GitHub Copilot
* Claude
* ChatGPT

These tools were primarily used for:

* Understanding unfamiliar development concepts
* Streamlit interface implementation
* Debugging and troubleshooting
* Code refactoring and optimization

The recommendation algorithms, data processing workflow, SQL analysis, model training, and project structure were studied, modified, tested, and integrated throughout the development process.

---

## 🔮 Future Improvements

* Hybrid Recommendation System
* Movie Poster Integration
* User Authentication
* Watchlist Functionality
* Real-Time Recommendation Updates
* Model Performance Monitoring
* Cloud Database Deployment

---

## 👨‍💻 Author

Rohit

Machine Learning and Data Analytics Enthusiast

---

## 📄 License

This project is intended for educational, learning, and portfolio purposes.
