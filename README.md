# coubdl
> A software to retrieve and download videos from coub
## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.
### Prerequisites
- Python 3.6 or above
- ffmpeg
#### Python Libs
- requests
- beautifulsoup4
- clint
## Installing
Linux (Ubuntu 18.04.2 LTS Bionic):
```bash
sudo apt update && sudo apt install -y ffmpeg
# If you already have python3 skip this part
sudo apt install -y python3 python3-pip
# Run the following commands inside the coubdl directory
pip3 install -r requirements.txt
# Run the program
python3 main.py https://coub.com/view/1vpqwl 3
```
Windows :
For installing ffmpeg refer to :
https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg#installing-ffmpeg-in-windows
For installing python 3 refer to:
https://www.python.org/downloads/
Then inside cmd and inside the coubdl directory
```
pip install -r requirements.txt
python main.py https://coub.com/view/1vpqwl 3
```

## Contributing

1. Fork it (<https://github.com/TheMightyBaguette/coubdl/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
