from jinja2 import Template
from flask import Flask, render_template
import json
import requests

app = Flask(__name__)

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
		bucketname=bucketname, list_example=[(obj['name'],f"http://localhost:5001/{bucketname}/{obj['name']}")for obj in objects],
		make_all=f"http://localhost:5001/{bucketname}"
		)

@app.route('/<bucketname>/display')
def display(bucketname):
	r = requests.get(f"http://localhost:5000/{bucketname}?list")
	objects = (r.json()['objects'])
	return render_template('display.html',
		show=bucketname+"/show_all_videos", 
		bucketname=bucketname, 
		list_example=[(obj['name'],f"http://localhost:5000/gifs/{bucketname}_{obj['name']}.gif",f"http://localhost:5000/gifs/{bucketname}_{obj['name']}.gif?delete") for obj in objects])

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=8080)