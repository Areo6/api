from flask import Flask, url_for, jsonify, request, json
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource
import status

app = Flask(__name__)
api = Api(app)

business_fields = {
    'id' : fields.Integer,
    'uri': fields.Url('business_endpoint'),
    'business_name' : fields.String,
    'business_type' : fields.String,
    'business_description' : fields.String
}

class BusinessModel(dict):
    def __init__(self, business_name,business_type,business_description):
        dict.__init__(self,business_name=business_name, business_type=business_type, business_description=business_description,id=0)

class Business():
    # stores the last value of id and and assigns Business instance stired in the dictionary.
    last_id = 0
    def __init__(self):
        # Initializes an empty dictionary
        self.businesses = {}
    
    def insert_business(self, business_name):
        # Creates a business with at least bus_name as argument
        self.__class__.last_id += 1
        business_name.id = self.__class__.last_id
        self.businesses[self.__class__.last_id] = business_name

    def get_business(self, id):
        # return a business with the specified id
        return  self.businesses[id]

    def delete_business(self, id):
        # Deletes a business given the specified id
        del self.businesses[id] 

business = Business()

class HeloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class Business1(Resource):
    def abort_if_business_does_not_exist(self, id):
        if id not in business.businesses:
            abort(status.HTTP_404_NOT_FOUND, message="Business {0} does not exist").format(id)

    @marshal_with(business_fields)
    def get_business(self,id):
        self.abort_if_business_does_not_exist(id)
        return business.get_business(id)

@app.route('/api/', methods=['GET'])
def get():
    return jsonify([v for v in business.businesses.values()])

@app.route('/api/businesses/', methods=['POST'])
def put():
    parser = reqparse.RequestParser()
    parser.add_argument('business_name', type = str, required = True, help = "businesss Name can't be blank.")
    parser.add_argument('business_type', type = str, required = False)
    parser.add_argument('business_description', type = str, required = False)
    args = parser.parse_args()
    buzness = BusinessModel(business_name = args['business_name'], business_type = args['business_type'], business_description = args['business_description'])
    business.insert_business(buzness)
    return json.dumps(buzness), status.HTTP_201_CREATED


# api.add_resource(BusinessList, '/api/businesses/')
# api.add_resource(Business1, '/api/businesses/<int:id>', endpoint='business_endpoint')

if __name__ == "__main__":
    app.run(debug = True)

