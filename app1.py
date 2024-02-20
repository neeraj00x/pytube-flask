from http.server import BaseHTTPRequestHandler, HTTPServer
from pytube import YouTube
from pathlib import Path
import os
import re
from urllib.parse import urlparse, parse_qs

class VideoDownloaderHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>YouTube Video Downloader</title>
        </head>
        <body>
            <h2>YouTube Video Downloader</h2>
            <form method="post">
                <label for="video_url">Enter YouTube Video URL:</label>
                <input type="text" name="video_url" required>
                <button type="submit">Download</button>
            </form>
            <p>{}</p>
        </body>
        </html>
        """

        self.wfile.write(html.format("").encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)

        youtube_url = params.get('video_url', [''])[0]

        if youtube_url:
            validate_video_url = (
                r'(https?://)?(www\.)?'
                '(youtube|youtu|youtube-nocookie)\.(com|be)/'
                '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
            valid_video_url = re.match(validate_video_url, youtube_url)

            if valid_video_url:
                url = YouTube(youtube_url)
                video = url.streams.get_highest_resolution()
                download_folder = str(os.path.join(Path.home(), "Downloads/Youtube_download"))
                video.download(download_folder)
                message = 'Video Downloaded Successfully!'
            else:
                message = 'Enter Valid YouTube Video URL!'
        else:
            message = 'Enter YouTube Video URL.'

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>YouTube Video Downloader</title>
        </head>
        <body>
            <h2>YouTube Video Downloader</h2>
            <form method="post">
                <label for="video_url">Enter YouTube Video URL:</label>
                <input type="text" name="video_url" required>
                <button type="submit">Download</button>
            </form>
            <p>{}</p>
        </body>
        </html>
        """

        self.wfile.write(html.format(message).encode('utf-8'))


def run():
    port = 8000
    server_address = ('', port)
    httpd = HTTPServer(server_address, VideoDownloaderHandler)
    print(f"Server running on port {port}")
    httpd.serve_forever()


if __name__ == '__main__':
    run()
