import json, requests, sys
import os
import youtube_dl
from flask import Flask, render_template, json, request, send_from_directory,request
import urllib
from bs4 import BeautifulSoup
import datetime
import re

year = datetime.date.today().year

# Flask app should start in global layout
app = Flask(__name__)

def make_savepath(title):
    return os.path.join("%s.mp3" % (title))

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html',year = year)


@app.route('/result', methods=['POST','GET'])
def result():
	search = request.form['search']
	query_string = urllib.parse.urlencode({"search_query": search})
	page = requests.get("http://www.youtube.com/results?" + query_string)
	soup = BeautifulSoup(page.content, 'html.parser')
	display = {}
	for vid in soup.find_all(class_="yt-lockup-content"):
		print(vid)
		#print(vid.find("a")["href"])
		#print(vid.find("a")["title"])
		print(vid.find(class_="yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2"))
		if vid.find(class_="yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2") is not None:
			des = vid.find(class_="yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2").get_text()
		else:
			des = " "
		link = "https://youtube.com"+vid.find("a")["href"]
		thumbnail = "http://img.youtube.com/vi/%s/0.jpg" % vid.find("a")["href"][9:]
		display[vid.find("a")["title"]] = [thumbnail,des,link]
	return render_template('result.html', display = display,year = year)

@app.route('/download', methods=['POST','GET'])
def download():
	url = request.form["song"]
	options = {
		'format': 'bestaudio/best',  # choice of quality
		'extractaudio': True,  # only keep the audio
		'audioformat': "mp3",  # convert to mp3
		'outtmpl': '%(id)s',  # name the file the ID of the video
		'noplaylist': True, }  # only download single song, not playlist

	ydl = youtube_dl.YoutubeDL(options)
	song_name = ydl.extract_info(url, download=False)
	savepath = make_savepath(song_name['title'].replace(" ", ""))
	savepath = re.sub('[^A-Za-z0-9]+', '', savepath)
	savepath = make_savepath((savepath))
	with ydl:
		result = ydl.extract_info(url, download=True)
		os.rename(result['id'], savepath)
		print("Downloaded and converted %s successfully!" % savepath)
		try:
			return send_from_directory(savepath, attachment_filename=savepath, as_attachment=True)
		except Exception as e:
			return str(e)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    print("Starting app on port %d" % port)

app.run(debug=False, port=port, host='0.0.0.0')