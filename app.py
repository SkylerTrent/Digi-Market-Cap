import os
import requests
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
  import env 

app = Flask(__name__)


app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)

r = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit=40&CMC_PRO_API_KEY=7d99530e-32dc-4fff-96ee-4b3811b660de')
results = r.json()
data = results['data']



@app.route('/')
@app.route('/coin_list')
def coin_list(): 
 
  return render_template("coin_list.html", data=data)


@app.route('/create_a_bag')
def create_a_bag():
  return render_template("create_a_bag.html", data=data)


@app.route('/add_to_bagz', methods=["POST"])
def add_to_bagz():
  users=mongo.db.users
  users.insert_one(request.form.to_dict())
  return redirect(url_for('get_my_bagz'))


@app.route('/get_my_bagz')
def get_my_bagz():
    
  return render_template("my_bagz.html", users=mongo.db.users.find(), data=data)


@app.route('/edit_bag/<bag_id>' )
def edit_bag(bag_id):
  the_bag = mongo.db.users.find_one({"_id": ObjectId(bag_id)})
    
  return render_template("edit_bag.html", bag=the_bag, data=data)


@app.route('/update_bag/<bag_id>', methods=["POST"])
def update_bag(bag_id):
  bag = mongo.db.users
  bag.update({'_id': ObjectId(bag_id)},
  {
    'assets': request.form.get('assets'),
    'amount': request.form.get('amount'),
    'price_paid': request.form.get('price_paid'),
    'date_of_purchase': request.form.get('date_of_purchase')
  })
  return redirect(url_for('get_my_bagz'))


@app.route('/delete_bag/<bag_id>')
def delete_bag(bag_id):
  mongo.db.users.remove({'_id': ObjectId(bag_id)})
  return redirect(url_for('get_my_bagz')) 

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), 
        port=(os.environ.get('PORT')),
        debug=True)