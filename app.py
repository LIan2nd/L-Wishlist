# Import Package
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

# Setup
client = MongoClient('mongodb+srv://Lroot:blokk@fullstacklearningx.p4dqs.mongodb.net/?retryWrites=true&w=majority&appName=fullstackLearningX')
db = client.dbsparta
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