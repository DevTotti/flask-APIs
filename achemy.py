from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
from sqlalchemy import create_engine
import json, simplejson
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'db.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)

class Media(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), unique=True)
	album = db.Column(db.String(100))
	artist = db.Column(db.String(100))
	genre = db.Column(db.String(100))
	duration = db.Column(db.Float)

	def __init__(self, name, artitst,album,genre,duration):
		self.name = name
		self.album = album
		self.artist = artitst
		self.genre = genre
		self.duration = duration

class MediaSchema(ma.Schema):
	class meta:
		fields = ('id','name','album','artist','genre','duration')


media_schema = MediaSchema(strict = True)

medias_schema = MediaSchema(many = True, strict = True)


@app.route('/media', methods = ['POST'])
def add_media():
	name = request.json['name']
	album = request.json['album']
	artist = request.json['artist']
	genre = request.json['genre']
	duration = request.json['duration']

	new_media = Media(name, artist, album, genre, duration)
	db.session.add(new_media)
	db.session.commit()

	return media_schema.jsonify(new_media)

@app.route('/media', methods = ['GET'])
def get_medias():
	all_media = Media.query.all()
	result = medias_schema.dump(all_media)
	return jsonify(result.data)


@app.route('/media/<id>', methods = ['GET'])
def get_single_media(id):
	media = Media.query.get(id)
	#result = medias_schema.dump(all_media)
	return media_schema.jsonify(media)
	

@app.route('/media/<id>', methods = ['PUT'])
def update_media(id):
	media = Media.query.get(id)
	name = request.json['name']
	album = request.json['album']
	artist = request.json['artist']
	genre = request.json['genre']
	duration = request.json['duration']

	#new_media = Media(name, artist, album, genre, duration)
	media.name = name
	media.album = album
	media.artist = artist
	media.genre = genre
	media.duration = duration

	#db.session.add(new_media)
	db.session.commit()

	return media_schema.jsonify(media)

if __name__ == '__main__':
	app.run(debug=True)