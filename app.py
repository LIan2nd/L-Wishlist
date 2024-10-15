# Import Package
import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

# Setup

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]
app = Flask(__name__)

# Home Route
@app.route('/')
def home() :
  return render_template('index.html')

# Post Wish Route
@app.route('/bucket', methods=["POST"])
def bucket() : 
  bucket = request.form["bucket"]
  print(bucket)
  count = db.wishlist.count_documents({})
  num = count + 1
  doc = {
    "num" : num,
    "wish" : bucket,
    "done" : 0,
  }
  db.wishlist.insert_one(doc)
  return jsonify({"msg": "Your Wishlist has been Saved! Good Luck"})

# Wish Done Route
@app.route('/bucket/done', methods=["POST"])
def bucket_done() :
  num = request.form["num"]
  db.wishlist.update_one({"num": int(num)}, {"$set": {"done" : 1}})
  return jsonify({"msg": "You're COOOLLL!!"})

# Get Wish Route
@app.route('/bucket', methods=["GET"])
def get_bucket() :
  wishlists = list(db.wishlist.find({}, {'_id': False}))
  return jsonify({"wishlists": wishlists,"msg": "GET BUCKET"})

# Delete Wish Route
@app.route('/delete', methods=["POST"])
def delete_bucket() : 
  num = request.form['num']
  db.wishlist.delete_one({"num": int(num)})
  return jsonify({"msg": "Your wishlist has been deleted"})

# Run App
port=5000
debug=True
if __name__ == "__main__" :
  app.run('0.0.0.0', port=port, debug=debug)