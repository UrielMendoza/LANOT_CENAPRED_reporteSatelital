import download_datasets
import base
import datetime

pathOutputL2A = '/home/lanotadm/data/LANOT_CENAPRED_reporteSatelital/sentinel2/tmp/'
start_date = datetime.datetime.now()
end_date = datetime.datetime.now()
region = 'volcanes'
tiles = base.tiles[region]
#download_datasets.search_and_download_datasets(tiles, start_date, end_date, pathOutputL2A, unzip=False)
daysDelta = 0
download_datasets.search_and_download_datasets(tiles, start_date - datetime.timedelta(days=daysDelta), end_date - datetime.timedelta(days=daysDelta), pathOutputL2A, unzip=False)