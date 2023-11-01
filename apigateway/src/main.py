import time
import logging
import requests

from ariadne import QueryType
from ariadne import MutationType
from ariadne import ObjectType
from ariadne import make_executable_schema
from ariadne import load_schema_from_path

from ariadne.asgi import GraphQL

from graphql.type import GraphQLResolveInfo

from starlette.middleware.cors import CORSMiddleware


type_defs = load_schema_from_path("./app/schema.graphql")

query = QueryType()
mutation = MutationType()

user = ObjectType("User")
plant = ObjectType("Plants")
construction = ObjectType("Constructions")


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')


@query.field("getFarm")
def resolve_get_user(obj, resolve_info: GraphQLResolveInfo, id):
    response = requests.get(f"http://render_service/farms/{id}")

    if response.status_code == 200:
        return response.json()

@query.field("getFarms")
def resolve_list_users(obj, resolve_info: GraphQLResolveInfo):
    response = requests.get(f"http://render_service/farms/")

    if response.status_code == 200:
        return response.json()
    
@query.field("getUser")
def resolve_get_user(obj, resolve_info: GraphQLResolveInfo, id):
    response = requests.get(f"http://construct_service/users/{id}")

    if response.status_code == 200:
        return response.json()

@query.field("getUsers")
def resolve_list_users(obj, resolve_info: GraphQLResolveInfo):
    response = requests.get(f"http://construct_service/users/")

    if response.status_code == 200:
        return response.json()


schema = make_executable_schema(type_defs, query, mutation, user, construction,plant)
app = CORSMiddleware(GraphQL(schema, debug=True), allow_origins=['*'], allow_methods=("GET", "OPTIONS"))