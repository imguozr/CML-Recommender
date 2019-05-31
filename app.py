import logging

import pymongo
from flask import Flask, jsonify
from flask_cors import CORS
import tensorflow as tf

from CML import CML
from utils import goodbooks

app = Flask(__name__)
CORS(app)

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.goodbooks
book_collection = db.books
rating_collection = db.ratings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

save_path = 'checkpoints/model'

user_item_matrix = goodbooks()
n_users, n_items = user_item_matrix.shape

model = CML(n_users, n_items,
            features=None, embed_dim=100,
            margin=1.9, clip_norm=1,
            master_learning_rate=0.1, use_rank_weight=True,
            use_cov_loss=False, cov_loss_weight=1)

sess = tf.Session()
saver = tf.train.Saver()
saver.restore(sess=sess, save_path=save_path)


@app.route('/user/<int:user_id>/rated_books', methods=['GET'])
def user_rated_books(user_id):
    logger.debug("User %s's rated books", user_id)
    book_list = []
    for items in rating_collection.find({'user_id': user_id}, {'_id': 0}):
        for book in book_collection.find({'book_id': items['book_id']}, {'_id': 0}):
            book['my_rating'] = items['rating']
            book_list.append(book)
    return jsonify(book_list)


@app.route('/user/<int:user_id>/ratings/top/<int:n>', methods=['GET'])
def get_top_n_ratings(user_id, n):
    book_list = []
    _, recom_list = sess.run(tf.nn.top_k(model.item_scores, n),
                             {model.score_user_ids: [user_id]})

    for item in recom_list[0]:
        for book in book_collection.find({'book_id': item.item()}, {'_id': 0}):
            book_list.append(book)

    return jsonify(book_list)


@app.route('/book/<int:book_id>/detail', methods=['GET'])
def get_book_details(book_id):
    logger.debug('Book %s detail', book_id)
    return jsonify(book_collection.find_one({'book_id': book_id}, {'_id': 0}))
