import requests
from dbconfig import tmdb

class TMDBService:
    @staticmethod
    def search_actors(query):
        url = f"{tmdb['base_url']}/search/person"
        headers = {
            "Authorization": f"Bearer {tmdb['bearer_token']}",
            "accept": "application/json"
        }
        params = {
            "query": query,
            "include_adult": False,
            "language": "en-US",
            "page": 1
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_actor_details(actor_id):
        url = f"{tmdb['base_url']}/person/{actor_id}"
        headers = {
            "Authorization": f"Bearer {tmdb['bearer_token']}",
            "accept": "application/json"
        }
        params = {
            "language": "en-US",
            "append_to_response": "combined_credits"
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()