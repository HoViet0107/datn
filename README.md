# Research and build a model to analyze user feedback on the TIKI e-commerce site

## Overview 

This project focuses on analyzing user feedback from the TIKI e-commerce site. The goal is to develop a machine learning model that can categorize and evaluate customer reviews, providing insights into product satisfaction. The entire process is implemented in Python.

## Table of Contents
- [Introduction](#introduction)
- [Technologies Used](#technologies-used)
- [Training and Analyzing](#training-and-analyzing)
- [Installation](#installation)
- [License](#license)

## Introduction

This project aims to build a sentiment analysis model that classifies user feedback into categories such as Positive, Neutral, and Negative. By leveraging machine learning and natural language processing (NLP), we can extract valuable insights from customer reviews.

Key Features:

- Data Collection: Scraping and processing user feedback from TIKI.
- Preprocessing: Cleaning and tokenizing Vietnamese text data.
- Feature Engineering: Applying TF-IDF vectorization for text representation.
- Model Training: Using Naïve Bayes and SVM for classification.
- Prediction: Providing an estimated rating based on review sentiment.
- Visualization: Displaying sentiment distributions and word clouds.

## Technologies Used  

The following tools and libraries are utilized in this project:

- **Python** (for data processing and modeling)
- **Pandas** (for data manipulation)
- **Scikit-learn** (for machine learning models)
- **TfidfVectorizer** (for feature extraction)
- **WordCloud** (for generating visual representations of common words)
- **PyVi** (for Vietnamese text processing, but has stopped developing try to use underthesea instead)

## Training and Analyzing  

Data Processing:

- Data Collection: Reviews are collected from TIKI using web scraping techniques.
- Text Preprocessing:
  - Standardizing text (removing special characters, lowercasing, etc.)
  - Tokenizing Vietnamese text using PyVi or Underthesea
  - Removing stopwords

Model Training:

- Feature Extraction: Convert text data into numerical vectors using TF-IDF.
- Training Models:
  - Naïve Bayes (for efficient text classification)
  - Support Vector Machine (for improved accuracy)
- Evaluation: Models are evaluated using accuracy.

Data Visualization:

- Rating Prediction: Estimate an average rating based on classified reviews.
- Pie Charts: Show sentiment distribution (Positive, Neutral, Negative).
- Word Clouds: Display frequently used words in each sentiment category.

## Installation  
1. Download and Install Python for Windows

   Link: [Download Python](https://www.python.org/downloads/)

2. Clone this repository to your local machine with cmd:
   
       git clone https://github.com/HoViet0107/datn.git
       cd datn
   
3. Open in Vscode
   
       code .
   
4. Open terminal
   
       Ctrl + "`"
        Or
       Toolbar -> Terminal -> New Terminal
   
   Check python:
       
       python --version
       
5. Create Virtual Environment(venv) and activate
        
        python -m venv .venv
        .\.venv\Scripts\activate
   
6. Install the required dependencies:
        
        pip install -r requirements.txt
    
7. Go to `main.ipynb` in `RecommenApp/` and run

## License  

This project is licensed under the MIT License - see the LICENSE file for details.
