# Deployment Notes

## Overview

This project was originally developed using the complete MovieLens dataset containing:

* 83,000+ Movies
* 33,000,000+ Ratings
* 330,000+ Users

The full dataset was used during data cleaning, preprocessing, exploratory data analysis, feature engineering, model training, and evaluation.

---

## Deployment Constraints

The original processed ratings dataset and Collaborative Filtering model were too large for GitHub and Streamlit Cloud deployment.

### Original Development Assets

| File                                 | Size     |
| ------------------------------------ | -------- |
| ratings_processed_main.csv           | ~1.15 GB |
| collaborative_filtering_svd_main.pkl | ~1.03 GB |

These files are retained locally and excluded from the repository using `.gitignore`.

---

## Deployment Version

To make deployment possible while preserving application functionality, optimized deployment files were created.

### Deployment Assets

| File                            | Size   |
| ------------------------------- | ------ |
| ratings_processed.csv           | ~87 MB |
| collaborative_filtering_svd.pkl | ~94 MB |

### Optimization Strategy

* A representative subset of the ratings dataset was used for deployment.
* The Collaborative Filtering (SVD) model was retrained using approximately 1 million ratings.
* Existing file names and application paths were preserved.
* No modifications were required in the Streamlit application code.

---

## Functionality Preserved

The deployed application includes:

* Popularity-Based Recommendations
* Content-Based Recommendations
* Collaborative Filtering Recommendations
* Interactive Analytics Dashboard
* Data Visualizations
* Movie Search and Recommendation Features

The recommendation workflow and user experience remain consistent with the original implementation.

---

## AI-Assisted Development

This project was developed primarily as a Machine Learning and Data Analytics project.

Since web application development was not my primary area of expertise, AI tools including GitHub Copilot, Claude, and ChatGPT were used to assist with:

* Streamlit dashboard development
* UI implementation
* Debugging and troubleshooting
* Deployment preparation
* Documentation support

All data processing, SQL workflows, exploratory analysis, recommendation algorithms, model training, testing, and project integration were performed and verified as part of the project development process.

---

## Repository Contents

The repository includes:

* SQL Scripts
* Jupyter Notebooks
* Data Processing Pipeline
* Recommendation Models
* Streamlit Dashboard
* Visualizations
* Documentation

Large development-only datasets and model artifacts have been intentionally excluded to ensure repository maintainability and successful deployment.
