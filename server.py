"""
Title: Server for Actor Management
Description: Flask server providing API for managing actors with CRUD operations and TMDB API integration for searching/importing actor data.
Author: Filipe Carvalho
"""

# Import necessary libraries
from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
from actorDAO import actorDAO
from tmdb_service import TMDBService 
import dbconfig as cfg

# Initialize Flask application
app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# Actor CRUD operations
@app.route('/actors')
@cross_origin()
def getAll():
    # Get all actors with support of pagination parameters
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
        
    all_actors = actorDAO.getAll()
    total = len(all_actors)
    start = (page - 1) * per_page
    end = start + per_page
    
    return jsonify({
        'actors': all_actors[start:end],
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    })

@app.route('/actors/<int:id>')
@cross_origin()
def findById(id):
    # Find actor by ID
    foundActor = actorDAO.findByID(id)
    return jsonify(foundActor)

@app.route('/actors', methods=['POST'])
@cross_origin()
def create_actor():
    # Create a new actor
    try:
        actor = request.get_json()
        
        if not actor:
            return jsonify({"error": "Bad Request", "details": "Request body must be JSON"}), 400

        required_fields = ['name', 'gender', 'dob', 'country']
        missing_fields = [field for field in required_fields if field not in actor]

        if missing_fields:
            return jsonify({
                "error": "Bad Request",
                "details": f"Missing fields: {', '.join(missing_fields)}"
            }), 400
        
        added_actor = actorDAO.create({
            "name": actor['name'],
            "gender": actor['gender'],
            "dob": actor['dob'],
            "country": actor['country']
        })        
        return jsonify(added_actor), 201

    except Exception as e:
        print(f"Error while creating actor: {e}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500


@app.route('/actors/<int:id>', methods=['PUT'])
@cross_origin()
def update(id):
    # Update an existing actor
    foundActor = actorDAO.findByID(id)
    if not foundActor:
        abort(404)
    
    if not request.json:
        abort(400)

    reqJson = request.json
    updates = {}

    for field in ['name', 'gender', 'dob', 'country']:
        if field in reqJson:
            updates[field] = reqJson[field]

    actorDAO.update(id, updates)
    return jsonify(actorDAO.findByID(id))
        
@app.route('/actors/<int:id>' , methods=['DELETE'])
@cross_origin()
def delete(id):
    # Delete an actor by ID
    actorDAO.delete(id)
    return jsonify({"done":True})

# Additional endpoints
@app.route('/countries')
@cross_origin()
def get_countries():   
    # Get all countries 
    countries = actorDAO.getAllCountries()
    return jsonify(countries)

# TMDB API integration
@app.route('/tmdb/search/<string:query>')
@cross_origin()
def search_tmdb(query):
    # Search for actors using TMDB API
    page = request.args.get('page', default=1, type=int)
    try:
        results = TMDBService.search_actors(query, page=page)
        return jsonify(results)
    except Exception as e:
        print(f"Error searching TMDB: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/tmdb/actor/<int:actor_id>')
@cross_origin()
def get_tmdb_actor(actor_id):
    # Get actor details from TMDB API
    try:
        actor_details = TMDBService.get_actor_details(actor_id)
        return jsonify(actor_details)
    except Exception as e:
        print(f"Error getting TMDB actor: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/tmdb/import/<int:actor_id>', methods=['POST'])
@cross_origin()
def import_tmdb_actor(actor_id):
    # Import actor details from TMDB API into actor table
    try:
        tmdb_actor = TMDBService.get_actor_details(actor_id)
        
        # Map TMDB data to actor in actor table
        actor_data = {
            "name": tmdb_actor.get("name"),
            "gender": "Male" if tmdb_actor.get("gender") == 2 else ("Female" if tmdb_actor.get("gender") == 1 else "Unknown"),
            "dob": tmdb_actor.get("birthday") or None,
            "country": tmdb_actor.get("place_of_birth", "").split(",")[-1].strip() if tmdb_actor.get("place_of_birth") else "Unknown"
        }
        
        imported_actor = actorDAO.create(actor_data)
        return jsonify(imported_actor), 201
        
    except Exception as e:
        print(f"Error importing actor: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__' :
    app.run(debug= True)