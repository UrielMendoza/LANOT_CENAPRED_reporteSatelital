import download_datasets
import base
import datetime

pathOutput = ''
start_date = datetime.datetime.now()
end_date = datetime.datetime.now()
region = 'volcanes'
tiles = base.tiles[region]
download_datasets.search_and_download_datasets(tiles, start_date, end_date, pathOutput, unzip=False)