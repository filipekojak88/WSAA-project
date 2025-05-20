from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
from actorDAO import actorDAO
from datetime import datetime
from tmdb_service import TMDBService 
import requests
import dbconfig as cfg


app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



@app.route('/')
@cross_origin()
def index():
    return "Hello, World!"

#curl "http://127.0.0.1:5000/actors"
@app.route('/actors')
@cross_origin()
def getAll():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    
    # Get all actors first (you might want to optimize this later)
    all_actors = actorDAO.getAll()
    
    # Calculate pagination
    total = len(all_actors)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_actors = all_actors[start:end]
    
    return jsonify({
        'actors': paginated_actors,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    })

#curl "http://127.0.0.1:5000/actors/2"
@app.route('/actors/<int:id>')
@cross_origin()
def findById(id):
    foundActor = actorDAO.findByID(id)

    return jsonify(foundActor)

#curl  -i -H "Content-Type:application/json" -X POST -d "{\"name\":\"hello\",\"gender\":\"someone\",\"dob\":1988/07/28}" http://127.0.0.1:5000/actors
@app.route('/actors', methods=['POST'])
@cross_origin()
def create_actor():
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
        
        actor_data = {
            "name": actor['name'],
            "gender": actor['gender'],
            "dob": actor['dob'],
            "country": actor['country']
        }

        added_actor = actorDAO.create(actor_data)
        return jsonify(added_actor), 201

    except Exception as e:
        print(f"Error while creating actor: {e}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500


#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"name\":\"hello\",\"gender\":\"someone\",\"dob\":1988/07/28}" http://127.0.0.1:5000/actors/1
@app.route('/actors/<int:id>', methods=['PUT'])
@cross_origin()
def update(id):
    foundActor = actorDAO.findByID(id)
    if not foundActor:
        abort(404)
    
    if not request.json:
        abort(400)

    reqJson = request.json

    if 'name' in reqJson:
        foundActor['name'] = reqJson['name']
    if 'gender' in reqJson:
        foundActor['gender'] = reqJson['gender']
    if 'dob' in reqJson:
        foundActor['dob'] = reqJson['dob']
    if 'country' in reqJson:
        foundActor['country'] = reqJson['country']

    actorDAO.update(id,foundActor)
    updatedActor = actorDAO.findByID(id)
    return jsonify(updatedActor)
        

@app.route('/actors/<int:id>' , methods=['DELETE'])
@cross_origin()
def delete(id):
    actorDAO.delete(id)
    return jsonify({"done":True})

@app.route('/countries')
@cross_origin()
def get_countries():    
    countries = actorDAO.getAllCountries()
    return jsonify(countries)

@app.route('/tmdb/search/<string:query>')
@cross_origin()
def search_tmdb(query):
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
    try:
        actor_details = TMDBService.get_actor_details(actor_id)
        return jsonify(actor_details)
    except Exception as e:
        print(f"Error getting TMDB actor: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/tmdb/import/<int:actor_id>', methods=['POST'])
@cross_origin()
def import_tmdb_actor(actor_id):
    try:
        # Get actor details from TMDB
        tmdb_actor = TMDBService.get_actor_details(actor_id)
        
        # Map TMDB data to your actor model
        actor_data = {
            "name": tmdb_actor.get("name"),
            "gender": "Male" if tmdb_actor.get("gender") == 2 else ("Female" if tmdb_actor.get("gender") == 1 else "Unknown"),
            "dob": tmdb_actor.get("birthday") or None,
            "country": tmdb_actor.get("place_of_birth", "").split(",")[-1].strip() if tmdb_actor.get("place_of_birth") else "Unknown"
        }
        
        # Save to your database
        added_actor = actorDAO.create(actor_data)
        return jsonify(added_actor), 201
        
    except Exception as e:
        print(f"Error importing actor: {e}")
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__' :
    app.run(debug= True)
