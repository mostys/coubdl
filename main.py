import coubdl as cb
import re
from clint import arguments
args = arguments.Args()
url = args.get(0)
if url is not None:
    regex = r"https://coub.com/[A-Za-z0-9]+/[A-Za-z0-9]{6}"
    if re.match(regex, url) is None:
        print("Please enter a valid coub.com url")
        exit(1)
    dw = cb.CoubDownloader(url)
    dw.dl()
    dw.merge()
    print("Exiting")
else:
    print("Usage : main.py <url>")
