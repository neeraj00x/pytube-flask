#
from flask import Flask, request, render_template
import requests, json

app = Flask(__name__)

def ext_video_id(video_url):
    fo = "https://youtu.be/"
    foo = "https://youtube.com/watch?v="
    bar = "https://www.youtube.com/watch?v="
    short = "https://www.youtube.com/shorts/"
    sshort = "https://youtube.com/shorts/"

    if fo in video_url:        video_id = video_url.replace(fo, '')
    elif foo in video_url:     video_id = video_url.replace(foo, '')
    elif bar in video_url:     video_id = video_url.replace(bar, '')
    elif short in video_url:   video_id = video_url.replace(short, '')
    elif sshort in video_url:  video_id = video_url.replace(sshort, '')
    else:                      video_id = ''

    return video_id


@app.route("/", methods=["GET","POST"])
def index():
    mesage = ''
    errorType = 0
    if request.method == 'POST' and 'video_url' in request.form:
        global youtubeUrl
        youtubeUrl = request.form["video_url"]
        video_id = ext_video_id(youtubeUrl)
        if(video_id):

            url = "https://yt1s.com/api/ajaxSearch/index"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,     like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
            }

            payload = {'q': youtubeUrl, 'vt': 'home'}   
            response = requests.post(url, data=payload, headers=headers)

            global json_response_obj
            json_response_obj = json.loads(response.text)
            links = json_response_obj["links"]
            mp4_res = {value["q"] + (' (' + value["size"]+')' if value["size"] else ''): key for key, value in links['mp4'].items()}
            mp3_res = {'MP3 ' + value["q"] + (' (' + value["size"]+')' if value["size"] else ''): key for key, value in links['mp3'].items()}
            media_res = list(mp4_res.keys()) + list(mp3_res.keys())
            res_keys = list(mp4_res.values()) +list(mp3_res.values())
            video_id = ext_video_id(youtubeUrl)
            return render_template('youtube.html', mesages = media_res, res_keys = res_keys, title = json_response_obj["title"], id= video_id)
        else:
            mesage = 'URL Error!'
            errorType = 0
    return render_template('index.html', mesage = mesage, errorType = errorType) 




@app.route("/download", methods=["GET","POST"])
def downloadVideo():
    mesage = ''
    errorType = 0
    if request.method == 'POST' and 'dropdown' in request.form:
        itag = request.form["dropdown"]
        if(itag):
            if itag == 'mp3128': k_post_payload = json_response_obj["links"]["mp3"]["mp3128"]["k"]
            else: k_post_payload = json_response_obj["links"]["mp4"][itag]["k"]
            video_id = ext_video_id(youtubeUrl)
            dl_link = ext_dl_link(video_id, youtubeUrl, k_post_payload)
            return render_template('download.html', mesages = mesage, title = json_response_obj["title"], id= video_id, link= dl_link["dlink"], ftype = dl_link["ftype"])
        else:
            mesage = 'No Video/Audio for Selected Resolution'
            errorType = 0
    return render_template('index.html', mesage = mesage, errorType = errorType) 



def ext_dl_link(video_id, video_url, k_post_payload):
    
    url = "https://yt1s.com/api/ajaxConvert/convert"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,     like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    payload = {'vid': video_id,'k': k_post_payload}
    response = requests.post(url, data=payload, headers=headers)
    video_dl_json = response.json()
    video_dl_link = video_dl_json

    return video_dl_link


if __name__ == "__main__":
    app.run(debug=True)