import requests
import currency_converter
import os

ConnectedToInternet = False

def DownloadURL(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

def UpdateData():

    global ConnectedToInternet

    try:
        URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip"
        SavePath = os.path.dirname(currency_converter.__file__) + "\eurofxref-hist.zip"
        DownloadURL(URL, SavePath)

        ConnectedToInternet = True

    except requests.exceptions.ConnectionError:
        ConnectedToInternet = False