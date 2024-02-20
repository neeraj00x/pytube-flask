#
from flask import Flask, request, render_template
from pytube import YouTube #pip install pytube https://pypi.org/project/pytube/
from pathlib import Path #pip install pathlib https://pypi.org/project/pathlib/
import os
import re
import requests, json

app = Flask(__name__)

@app.route("/download", methods=["GET","POST"])
def downloadVideo():
    mesage = ''
    errorType = 0
    if request.method == 'POST' and 'video_url' in request.form:
        youtubeUrl = request.form["video_url"]
        if(youtubeUrl):
            validateVideoUrl = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
            validVideoUrl = re.match(validateVideoUrl, youtubeUrl)
            if validVideoUrl:
                url = YouTube(youtubeUrl)
                video = url.streams.get_highest_resolution()
                downloadFolder = str(os.path.join(Path.home(), "Downloads/Youtube_download"))
                video.download()
                mesage = 'Video Downloaded Successfully!'
                errorType = 1
            else:
                mesage = 'Enter Valid YouTube Video URL!'
                errorType = 0

            url = "https://yt1s.com/api/ajaxSearch/index"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,     like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
            }

            payload = {'q': youtubeUrl, 'vt': 'home'}   
            response = requests.post(url, data=payload, headers=headers)

            json_response_obj = json.loads(response.text)
            #print(json_response_obj)
            return json_response_obj


            
        else:
            mesage = 'Enter YouTube Video Url.'
            errorType = 0
    return render_template('youtube.html', mesage = mesage, errorType = errorType) 

# if __name__ == "__main__":
#     app.run(port='8000')