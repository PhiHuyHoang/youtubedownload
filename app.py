import json, requests, sys
import json
import os
import youtube_dl
from flask import Flask, render_template, json, request
from flask import request
from flask import make_response
from random import choice, randint
import urllib
from bs4 import BeautifulSoup
# Flask app should start in global layout
app = Flask(__name__)

link = []
title = []
display = {}

def make_savepath(title):
    return os.path.join("%s.mp3" % (title))

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')


@app.route('/webhook', methods=['POST','GET'])
def webhook():
	search = request.form['lname']
	query_string = urllib.parse.urlencode({"search_query" : search})
	page = requests.get("http://www.youtube.com/results?" + query_string)
	soup = BeautifulSoup(page.content, 'html.parser')
	for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
		link.append('https://www.youtube.com' + vid['href'])
		title.append(vid['title'])
		display[vid['title']] = 'https://www.youtube.com' + vid['href']
	return render_template('result.html', display = display )

@app.route('/download', methods=['POST','GET'])
def download():
	options = {
	    'format': 'bestaudio/best', # choice of quality
	    'extractaudio' : True,      # only keep the audio
	    'audioformat' : "mp3",      # convert to mp3
	    'outtmpl': '%(id)s',        # name the file the ID of the video
	    'noplaylist' : True,}       # only download single song, not playlist

	ydl = youtube_dl.YoutubeDL(options)
	i = int(request.form['lname'])
	print(link[i],':','Chosen link')
	savepath = make_savepath(title[i])
	with ydl:
	    result = ydl.extract_info(link[int(input())], download=True)
	    os.rename(result['id'], savepath)
	    print("Downloaded and converted %s successfully!" % savepath)

if __name__ == '__main__':
    app.run()