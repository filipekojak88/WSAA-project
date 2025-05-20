"""
Title: TMDB Service
Description: This module provides a service to interact with the TMDB API for searching and retrieving actor details.
Author: Filipe Carvalho
"""

# Import necessary libraries
import requests
import dbconfig as cfg

class TMDBService:
    """Service to interact with TMDB API"""
    
    # API Configuration
    headers = {
        "Authorization": f"Bearer {cfg.tmdb['bearer_token']}",
        "accept": "application/json"
    }
    default_params= {"language": "en-US"}

    @staticmethod
    def search_actors(query, page=1):
        # Search for actors by name
        url = f"{cfg.tmdb['base_url']}/search/person"
        
        params = {
            **TMDBService.default_params,
            "query": query,
            "include_adult": False,
            "language": "en-US",
            "page": page
      }
    
        response = requests.get(
            url, 
            headers=TMDBService.headers, 
            params=params
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_actor_details(actor_id):
        # Get detailed information about an actor
        url = f"{cfg.tmdb['base_url']}/person/{actor_id}"
        params = {
            **TMDBService.default_params,
            "append_to_response": "combined_credits"
        }
        
        response = requests.get(
            url, 
            headers=TMDBService.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()