# server_2.py - Test server for TMDb API integration
from flask import Flask, request, jsonify
import requests
from functools import wraps
import logging

app = Flask(__name__)

# Configuration
TMDB_API_KEY = "f2e9f772126f1b0d2dd7c2bb472a9bf2"  # Replace with your actual key
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logger.info(f"Incoming request: {request.method} {request.url}")
        logger.info(f"Headers: {dict(request.headers)}")
        logger.info(f"Query params: {request.args}")
        if request.json:
            logger.info(f"Request body: {request.json}")
        return f(*args, **kwargs)
    return decorated_function

@app.route('/actor/<int:actor_id>', methods=['GET'])
@log_request
def get_actor(actor_id):
    """
    Fetch actor details from TMDb API
    Example: GET /actor/31 (Tom Hanks)
    """
    try:
        # Fetch basic actor info
        actor_url = f"{TMDB_BASE_URL}/person/{actor_id}"
        params = {
            'api_key': TMDB_API_KEY,
            'language': 'en-US'
        }
        
        response = requests.get(actor_url, params=params)
        response.raise_for_status()
        actor_data = response.json()
        
        # Fetch movie credits
        credits_url = f"{TMDB_BASE_URL}/person/{actor_id}/movie_credits"
        credits_response = requests.get(credits_url, params=params)
        credits_response.raise_for_status()
        credits_data = credits_response.json()
        
        # Structure the response
        result = {
            'id': actor_data.get('id'),
            'name': actor_data.get('name'),
            'biography': actor_data.get('biography'),
            'birthday': actor_data.get('birthday'),
            'profile_image': f"https://image.tmdb.org/t/p/original{actor_data.get('profile_path', '')}",
            'movies': [{
                'id': movie.get('id'),
                'title': movie.get('title'),
                'character': movie.get('character'),
                'release_date': movie.get('release_date'),
                'poster': f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}"
            } for movie in credits_data.get('cast', []) if movie.get('media_type') != 'tv']
        }
        
        logger.info(f"Successfully fetched data for actor ID: {actor_id}")
        return jsonify(result), 200
        
    except requests.exceptions.HTTPError as err:
        logger.error(f"TMDb API error: {str(err)}")
        return jsonify({'error': str(err)}), err.response.status_code
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/search/actor', methods=['GET'])
@log_request
def search_actor():
    """
    Search for actors by name
    Example: GET /search/actor?query=Tom+Hanks
    """
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query parameter "query" is required'}), 400
    
    try:
        search_url = f"{TMDB_BASE_URL}/search/person"
        params = {
            'api_key': TMDB_API_KEY,
            'query': query,
            'language': 'en-US'
        }
        
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        search_data = response.json()
        
        results = [{
            'id': person.get('id'),
            'name': person.get('name'),
            'known_for': person.get('known_for_department'),
            'profile_image': f"https://image.tmdb.org/t/p/original{person.get('profile_path', '')}" if person.get('profile_path') else None,
            'popularity': person.get('popularity')
        } for person in search_data.get('results', [])]
        
        logger.info(f"Found {len(results)} results for query: {query}")
        return jsonify({'results': results}), 200
        
    except requests.exceptions.HTTPError as err:
        logger.error(f"TMDb API error: {str(err)}")
        return jsonify({'error': str(err)}), err.response.status_code
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)