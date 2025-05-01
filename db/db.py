from py2neo import Graph
from dotenv import load_dotenv
from os import getenv

load_dotenv()

graph = Graph(f"bolt://{getenv('DB_HOST')}:{getenv('DB_PORT')}", auth=(getenv('DB_USER'), getenv('DB_PASS')))
