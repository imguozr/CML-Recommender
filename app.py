import json
import pymongo
import logging

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
        for book in book_collection.find({'book_id': items['book_id']}, {'_id': 0}):
            book['my_rating'] = items['rating']
            book_items.append(book)
    return jsonify(book_items)


@app.route('/user/<int:user_id>/add_ratings', methods=['POST'])
def add_ratings(user_id):
    pass


@app.route('/user/<int:user_id>/ratings/top/<int:n>', methods=['GET'])
def get_top_n_ratings(user_id, n):
    pass


@app.route('/book/<int:book_id>/detail', methods=['GET'])
def get_book_details(book_id):
    logger.debug('Book %s detail', book_id)
    return jsonify(book_collection.find_one({'book_id': book_id}, {'_id': 0}))
