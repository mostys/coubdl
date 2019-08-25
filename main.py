import coubdl as cb
import re
from clint import arguments

args = arguments.Args()
url = args.get(0)
loop = args.get(1)
if url is not None:
    regex = r"https://coub.com/[A-Za-z0-9]+/[A-Za-z0-9]{6}"
    if re.match(regex, url) is None:
        print("Please enter a valid coub.com url")
        exit(1)
    if loop is not None and str(loop) != "" and len(loop) > 0 and len(args) > 1:
        dw = cb.CoubDownloader(url, loop)
    else:
        dw = cb.CoubDownloader(url, "1")
    dw.dl()
    dw.merge()
    print("Exiting")
else:
    print("Usage : coubdl.exe <url> <loop>")
    print("Example : coubdl.exe https://coub.com/view/1vpqwl 3")
