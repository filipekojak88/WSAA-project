"""
Title: Database Configuration
Description: This file contains the configuration settings for connecting to a MySQL database and TMDB API.
#Author: Filipe Carvalho
"""

# MySQL database configuration
mysql = {
    'host':"filipekojak88.mysql.pythonanywhere-services.com",
    'user':"filipekojak88",
    'password':"280788WSAAproject",
    'database':"filipekojak88$actors_db"
}

# TMDB API configuration
tmdb = {
    'api_key': "f2e9f772126f1b0d2dd7c2bb472a9bf2",
    'bearer_token': "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmMmU5Zjc3MjEyNmYxYjBkMmRkN2MyYmI0NzJhOWJmMiIsIm5iZiI6MTc0NzYwMzY4MS44MjIsInN1YiI6IjY4MmE1MGUxMTI0NTg1NTkxN2RiMmI2MyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.FmxYIrubjlPiothTRWp4xHqSy0yVii_EO-2Q_00xySE",
    'base_url': "https://api.themoviedb.org/3"
}
