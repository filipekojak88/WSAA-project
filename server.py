from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
from actorDAO import actorDAO
from datetime import datetime

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


#app = Flask(__name__)

@app.route('/')
@cross_origin()
def index():
    return "Hello, World!"

#curl "http://127.0.0.1:5000/actors"
@app.route('/actors')
@cross_origin()
def getAll():
    #print("in getall")
    results = actorDAO.getAll()
    return jsonify(results)

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

        required_fields = ['name', 'gender', 'dob', 'country_id']
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
            "country": actor['country_id']
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
    if 'dob' in reqJson:
        try:
            dob = datetime.strptime(reqJson['dob'], "%Y-%m-%d").date()
        except ValueError:
            abort(400)  # Invalid date format

    if 'name' in reqJson:
        foundActor['name'] = reqJson['name']
    if 'gender' in reqJson:
        foundActor['gender'] = reqJson['gender']
    if 'dob' in reqJson:
        foundActor['dob'] = reqJson['dob']
    actorDAO.update(id,foundActor)
    return jsonify(foundActor)
        

    

@app.route('/actors/<int:id>' , methods=['DELETE'])
@cross_origin()
def delete(id):
    actorDAO.delete(id)
    return jsonify({"done":True})

@app.route('/countries')
def get_countries():
    from actorDAO import actorDAO
    countries = actorDAO.getAllCountries()
    return jsonify(countries)


if __name__ == '__main__' :
    app.run(debug= True)
