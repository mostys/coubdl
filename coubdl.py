import requests
import json
from bs4 import BeautifulSoup
import subprocess
import os
from clint.textui import progress


class CoubDownloader:
    def __init__(self, url, loop):
        if "embed" in url:
            self.url = url.replace("embed", "view")
        else:
            self.url = url
        self.loop = int(loop)
        self.coubid = self.url[22:]
        self.videoname = self.coubid + "_video"
        self.audioname = self.coubid + "_audio.mp3"

    def datadl(self, url, filetype):
        filename = self.audioname if filetype == "audio" else self.videoname
        r = requests.get(url, allow_redirects=True, stream=True)
        with open(filename, "wb") as f:
            total_length = int(r.headers.get("content-length"))
            for chunk in progress.bar(
                r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1
            ):
                if chunk:
                    f.write(chunk)
                    f.flush()
        return filename

    def fixencoding(self):
        filename = self.videoname
        with open(filename, "rb") as f1:
            f1.seek(2)
            with open(filename + ".mp4", "wb") as f2:
                f2.write(b"\x00\x00")
                for chunk in iter(lambda: f1.read(16384), ""):
                    if chunk == b"":
                        break
                    f2.write(chunk)
        self.videoname = filename + ".mp4"
        return None

    def retrieve_data(self, json, filetype):
        filename = ""
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
            print("Error type not found in json (no high/med quality)")
            exit(1)
        return filename

    def merge(self):
        with open("tempvid.txt", "w", encoding="utf8") as f:
            for i in range(1, self.loop + 1):
                f.write("file "+self.videoname+" \n")
        cmd = "ffmpeg -f concat -safe 0 -i tempvid.txt -i {} -shortest {}.mp4 -y".format(
            self.audioname, self.coubid
        )
        subprocess.call(cmd, shell=True)
        os.remove(self.videoname.replace(".mp4", ""))
        os.remove(self.videoname)
        os.remove(self.audioname)
        if self.loop > 2:
            os.remove("tempvid.txt")
        print("Muxing Done with ffmpeg")

    def dl(self):
        r = requests.get(self.url)
        html = BeautifulSoup(r.text, features="html.parser")
        assert r.status_code == 200
        cbdata = html.find(id="coubPageCoubJson").get_text()
        cbdata = json.loads(cbdata)
        html5 = cbdata["file_versions"]["html5"]
        video = html5["video"]
        audio = html5["audio"]
        self.retrieve_data(video, "video")
        self.retrieve_data(audio, "audio")
        self.fixencoding()
