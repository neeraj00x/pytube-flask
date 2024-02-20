import requests, json

def yt1s_api_payload_k(video_url):
    
    url = "https://yt1s.com/api/ajaxSearch/index"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,     like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    payload = {'q': video_url, 'vt': 'home'}   
    response = requests.post(url, data=payload, headers=headers)

    json_response_obj = json.loads(response.text)
    #print(json_response_obj)
    return json_response_obj

a = yt1s_api_payload_k("https://www.youtube.com/watch?v=vIcnjctQowY")

print(a)
