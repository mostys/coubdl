import requests
import json
from bs4 import BeautifulSoup
import subprocess
from clint.textui import progress


class CoubDownloader:
    def __init__(self, url):
        # TODO: Regex to check the url and change embed to view
        self.url = url
        self.videoname = self.url[22:]+"_video"
        self.audioname = self.url[22:]+"_audio.mp3"

    def datadl(self, url, filetype):
        filename = self.audioname if filetype == "audio" else self.videoname
        r = requests.get(url, allow_redirects=True, stream=True)
        with open(filename, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
                if chunk:
                    f.write(chunk)
                    f.flush()
        return filename

    def fixencoding(self):
        filename = self.videoname
        with open(filename, 'rb') as f1:
            f1.seek(2)
            with open(filename + ".mp4", 'wb') as f2:
                f2.write(b'\x00\x00')
                for chunk in iter(lambda: f1.read(16384), ''):
                    if chunk == b'':
                        break
                    f2.write(chunk)
        self.videoname = filename + ".mp4"
        return None

    def retrieve_data(self, json, filetype):
        filename = ''
        if "high" in json:
            try:
                url = json["high"]["url"]
                print(url)
                filename = self.datadl(url, filetype)
            except Exception as e:
                print(e)

        elif "med" in json:
            try:
                url = json["med"]["url"]
                filename = self.datadl(url, filetype)
            except Exception as e:
                print(e)
        else:
            print("Erreur type flux")
            exit(1)
        return filename

    def merge(self):
        cmd = 'ffmpeg -i {0} -i {1} -filter_complex " [1:0] apad " -shortest output.mp4'.format(
            self.videoname, self.audioname)
        subprocess.call(cmd, shell=True)
        print('Muxing Done')

    def dl(self):
        r = requests.get(self.url)
        # print(r.status_code)
        html = BeautifulSoup(r.text, features="html.parser")
        cbdata = html.find(id="coubPageCoubJson").get_text()
        text = open("test.json", "w")
        print(cbdata, file=text)
        cbdata = json.loads(cbdata)
        html5 = cbdata["file_versions"]["html5"]
        video = html5["video"]
        audio = html5["audio"]
        self.retrieve_data(video, "video")
        self.retrieve_data(audio, "audio")
        self.fixencoding()
        print("STOP")
