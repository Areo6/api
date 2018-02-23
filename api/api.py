from flask import Flask, url_for, jsonify, request, json, make_response
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource
from datetime import datetime
from models import BusinessModel, UserModel
import status
from pytz import utc

app = Flask(__name__)
api = Api(app)

class UserManager():
    last_id = 0
    def __init__(self):
        self.user = {}

    def register(self, user):
        self.__class__.last_id += 1
        user.id = self.__class__.last_id
        self.user[self.__class__.last_id] = user
    def login(self, id):
        return self.user[id]
    def logout(self, id):
        del self.user[id]

class BusinessManager():
    last_id = 0
    def __init__(self):
        self.businesses = {}
    def insert_business(self, business):
        self.__class__.last_id += 1
        business.id = self.__class__.last_id
        self.businesses[self.__class__.last_id] = business
    def get_business(self, id):
        return self.businesses[id]
    def delete_business(self, id):
        del self.businesses[id]

business_fields = {
    'id': fields.Integer,
    'uri': fields.Url('business_endpoint'),
    'business_name': fields.String,
    'business_type': fields.String,
    'business_desc': fields.String
}
business_manager = BusinessManager()
user_fields = {
    'id': fields.Integer,
    'uri': fields.Url('user_endpoint'),
    'name': fields.String,
    'email': fields.String,
    'password': fields.String
}
user_manager = UserManager()

class User(Resource):
    def abort_if_user_doesnt_exist(self, id):
        if id not in user_manager.user:
            abort(
            status.HTTP_404_NOT_FOUND,
            message="Business {0} doesn't exist".format(id))
    @marshal_with(user_fields)
    def get(self, id):
        self.abort_if_user_doesnt_exist(id)
        return user_manager.login(id)

    def delete(self, id):
        self.abort_if_user_doesnt_exist(id)
        user_manager.logout(id)
        return '', status.HTTP_403_FORBIDDEN
    @marshal_with(user_fields)
    def patch(self, id):
        self.abort_if_user_doesnt_exist(id)
        user = user_manager.login(id)
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        if 'name' in args:
            user.name = args['name']
        if 'email' in args:
            user.email = args['email']
        if 'password' in args:
            user.password = args['password']
        return user

class Business(Resource):
    '''This class provides the routing mecanism to business endpoints'''

    def abort_if_business_doesnt_exist(self, id):
        if id not in business_manager.businesses:
            abort(
            status.HTTP_404_NOT_FOUND,
            message="Business {0} doesn't exist".format(id))

    @marshal_with(business_fields)
    def get(self, id):
        self.abort_if_business_doesnt_exist(id)
        return business_manager.get_business(id)

    def delete(self, id):
        self.abort_if_business_doesnt_exist(id)
        business_manager.delete_business(id)
        return '', status.HTTP_204_NO_CONTENT

    @marshal_with(business_fields)
    def patch(self, id):
        self.abort_if_business_doesnt_exist(id)
        business = business_manager.get_business(id)
        parser = reqparse.RequestParser()
        parser.add_argument('business_name', type=str)
        parser.add_argument('business_type', type=str)
        parser.add_argument('business_desc', type=str)
        args = parser.parse_args()
        if 'business_name' in args:
            business.business_name = args['business_name']
        if 'business_type' in args:
            business.business_type = args['business_type']
        if 'business_desc' in args:
            business.business_desc = args['business_type']
        return business

class BusinessList(Resource):
    '''This class provides the routing mecanism to business endpoints'''

    @marshal_with(business_fields)
    def get(self):
        return [v for v in business_manager.businesses.values()]

    @marshal_with(business_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('business_name', type=str, required=True, help='Business Name cannot be blank!')
        parser.add_argument('business_type', type=str, required=True, help='Business Type cannot be blank!')
        parser.add_argument('business_desc', type=str, required=True, help='Business Description cannot be blank!')
        args = parser.parse_args()
        business = BusinessModel(
        business_name=args['business_name'],
        business_type=args['business_type'],
        business_desc=args['business_desc'])
        business_manager.insert_business(business)
        return business, status.HTTP_201_CREATED
class UserList(Resource):
    '''This class provides the routing mecanism to user endpoints'''

    @marshal_with(user_fields)
    def get(self):
        # displays all the users for the admin for example
        return [v for v in user_manager.user.values()]
    @marshal_with(user_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name cannot be blank!')
        parser.add_argument('email', type=str, required=True, help='Email Type cannot be blank!')
        parser.add_argument('password', type=str, required=True, help='Password Description cannot be blank!')
        args = parser.parse_args()
        user = UserModel(
        name=args['name'],
        email=args['email'],        
        password=args['password'])
        user_manager.register(user)
        return user, status.HTTP_201_CREATED

api.add_resource(BusinessList, '/api/businesses/')
api.add_resource(Business, '/api/businesses/<int:id>', endpoint='business_endpoint')
api.add_resource(User, '/api/auth/login/<int:id>', endpoint='user_endpoint')
api.add_resource(UserList, '/api/auth/register/')

if __name__ == "__main__":
    app.run(host=(0.0.0.0), debug = True)

