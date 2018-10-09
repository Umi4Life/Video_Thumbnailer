#!/usr/bin/env python3

from jinja2 import Template
from flask import Flask, render_template, jsonify, request
import json
import os
import requests
from flask_cors import CORS

HOST = os.getenv("frontend", "localhost")
app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def index():
	r = requests.get("http://localhost:5000/debug?get")
	objects = (r.json()['buckets'])
	return render_template('index.html', list_example=objects)

@app.route('/<bucketname>/show_all_videos')
def show(bucketname):
	r = requests.get(f"http://localhost:5000/{bucketname}?list")
	objects = (r.json()['objects'])
	return render_template('show.html',
		display=bucketname+"/display", 
		bucketname=bucketname, list_example=[(  obj['name'],
												f"http://localhost:5001/{bucketname}/{obj['name']}",
												f"http://localhost:8080/{bucketname}/{obj['name']}/delete")for obj in objects],
		make_all=f"http://localhost:5001/{bucketname}"
		)

@app.route('/<bucketname>/display')
def display(bucketname):
	r = requests.get(f"http://localhost:5000/{bucketname}?list")
	objects = (r.json()['objects'])
	return render_template('display.html',
		delete_all=f"http://localhost:8080/{bucketname}/delete_all",
		show=bucketname+"/show_all_videos", 
		bucketname=bucketname, 
		list_example=[(obj['name'],f"http://localhost:5000/gifs/{bucketname}_{obj['name']}.gif",f"http://localhost:8080/{bucketname}/{obj['name']}/delete") for obj in objects])

@app.route('/<bucketname>/<objectname>/delete')
def delete(bucketname, objectname):
	r = requests.delete(f"http://localhost:5000/gifs/{bucketname}_{objectname}.gif?delete")
	return jsonify({'status': 'OK'})
@app.route('/<bucketname>/delete_all')
def delete_all(bucketname):
	r = requests.get(f"http://localhost:5000/{bucketname}?list")
	objects = (r.json()['objects'])
	for obj in objects:
		requests.delete(f"http://localhost:5000/gifs/{bucketname}_{obj['name']}.gif?delete")
	return jsonify({'status': 'OK'})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=8080)