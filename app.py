import json
import pymongo
import logging

from flask import Flask, request
from flask import Blueprint

app = Flask(__name__)
# main = Blueprint('main', __name__)
# app.register_blueprint(main)

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.goodbooks
book_collection = db.books
rating_collection = db.ratings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.route('/user/<int:user_id>/rated_books', methods=['GET'])
def user_rated_books(user_id):
    logger.debug("User %s's rated books", user_id)
    book_items = []
    for items in rating_collection.find({'user_id': user_id}, {'_id': 0}):
        book_items.append(items)
    return json.dumps(book_items)


@app.route('/user/<int:user_id>/add_ratings', methods=['POST'])
def add_ratings(user_id):
    pass


@app.route('/user/<int:user_id>/ratings/top/<int:n>', methods=['GET'])
def get_top_n_ratings(user_id, n):
    pass


@app.route('/book/<int:book_id>/details', methods=['GET'])
def get_book_details(book_id):
    logger.debug('Book %s details', book_id)
    return json.dumps(book_collection.find_one({'book_id': book_id}, {'_id': 0}))
