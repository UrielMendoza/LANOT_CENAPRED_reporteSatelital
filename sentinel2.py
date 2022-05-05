import download_datasets
import base
import datetime
from glob import escape, glob
import os
from osgeo import gdal,osr

def obtieneFecha(pathDir):
    fecha = pathDir.split('/')[-1].split('.')[0].split('_')[2]
    fecha = datetime.datetime.strptime(fecha,'%Y%m%dT%H%M%S')
    return fecha.strftime('%Y-%m-%dT%H:%M:%S')

def obtieneFechaImaProc(pathDir):
    fecha = pathDir.split('/')[-1].split('.')[0].split('_')[-1]
    #fecha = datetime.datetime.strptime(fecha,'%Y%m%dT%H%M%S')
    return fecha

def obtieneTile(pathArchivo):
    tile = pathArchivo.split('/')[-1].split('_')[5]
    return tile

def obtieneAnio(path):
   anio = path.split('/')[-1].split('_')[2][:4]
   return anio

def nomDir(pathInput,nivel):
    archivo = pathInput.split('/')[-1].split('.')[0]
    if nivel == 'L2A':
        return archivo+'.SAFE'
    elif nivel == 'L1C':
        return archivo+'.SAFE'
    elif nivel == 'L1C_resampled':
        return archivo+'.resampled.data'

def aperturaDS(pathBand):
    ds = gdal.Open(pathBand)
    return ds

def imgToGeoTIF(ds,tif,pathOutput):
    print("Pasando a tif: "+pathOutput+tif+'.tif')
    gdal.Translate(pathOutput+tif+'.tif',ds)

def tipoCompresion(pathInput):
    compresion = pathInput.split('/')[-1].split('.')[-1]
    return compresion

def descomprime(pathInput,pathOutput):
    compresion = tipoCompresion(pathInput) 
    if compresion == 'gz':
        os.system('tar -xvzf '+pathInput+' -C '+pathOutput)
    elif compresion == 'zip':
        os.system('unzip '+pathInput+' -d '+pathOutput)

def listaBandas(pathInput,nivel,resolucion,banda):
    if nivel == 'L2A':
        archivoBanda = glob(pathInput+'/GRANULE/L2*/IMG_DATA/'+resolucion+'/*'+banda+'*.jp2')
    elif nivel == 'L1C':
        archivoBanda = glob(pathInput+'/GRANULE/L1C*/IMG_DATA/*.jp2')
    elif nivel == 'L1C_resampled':
        archivoBanda = glob(pathInput+'/'+banda+'.img')
    print("Archivo usado:"+archivoBanda[0])
    return archivoBanda[0]

def RGB_TC(nivel,resolucion,pathInput,tile,pathOutputGeoTiff):
    dirTC = listaBandas(pathInput,nivel,resolucion,'TCI')
    nombre = pathOutputGeoTiff+'TC_'+tile+'_latest.tif'
    os.system('gdal_translate '+dirTC+' '+nombre)

def RGB(r,g,b,tile,pathOutputGeoTiff):
    nombre = pathOutputGeoTiff+'SWIR_'+tile+'_latest.tif'
    #os.system('gdal_merge.py -ot uint16 -a_nodata 0 -separate -co PHOTOMETRIC=RGB -o '+nombre+' '+r+' '+g+' '+b)
    os.system('gdalbuildvrt -separate stack.vrt '+r+' '+g+' '+b)
    os.system('gdal_translate -of GTiff -ot Byte -scale 0 255 stack.vrt '+nombre)    

""" def generaDate(pathLatest,fecha):
    f = open('latest.csv','r') """

def escribeDatos(pathOutput,sector,ultimo,dia,hora):
    file = open(pathOutput+sector+"_date_latest.txt","w")
    file.write(ultimo+","+dia+","+hora)
    file.close()

pathL2A = '/home/lanotadm/data/LANOT_CENAPRED_reporteSatelital/sentinel2/L2A/'
pathLatest = '/home/lanotadm/data/LANOT_CENAPRED_reporteSatelital/sentinel2/latest/'
pathTmp = '/home/lanotadm/data/LANOT_CENAPRED_reporteSatelital/sentinel2/tmp/'
start_date = datetime.datetime.now()
end_date = datetime.datetime.now()
region = 'volcanes'
bandas20m = ('B04','B8A','B12')
tiles = base.tiles[region]
#download_datasets.search_and_download_datasets(tiles, start_date, end_date, pathL2A, unzip=False)
daysDelta = 2
download_datasets.search_and_download_datasets(tiles, start_date - datetime.timedelta(days=daysDelta), end_date - datetime.timedelta(days=daysDelta), pathL2A, unzip=False)

tilesDirs = glob(pathL2A+'*')

if len(tilesDirs) != 0:
    for tileDir in tilesDirs:
        archivo = glob(tileDir+'/*')[0]

        size = os.path.getsize(archivo)/1000000
        print('Tamaño:',size)

        if size >= 100:

            print('Procesando: '+archivo)
            fecha = obtieneFecha(archivo)
            dia = fecha.split('T')[0]
            hora = fecha.split('T')[1]
            fechaImaProc = obtieneFechaImaProc(archivo)
            tile = obtieneTile(archivo)
            anio = obtieneAnio(archivo)
            dirI = nomDir(archivo,'L2A')

            print("Fecha: "+fecha)
            print("Tile: "+tile)

            descomprime(archivo,pathTmp)

            for banda20 in bandas20m:
                dirB20 = listaBandas(pathTmp+dirI,'L2A','R20m',banda20)
                dsB20 = aperturaDS(dirB20)
                imgToGeoTIF(dsB20,banda20,pathTmp)
            r = pathTmp+bandas20m[2]+'.tif'
            g = pathTmp+bandas20m[1]+'.tif'
            b = pathTmp+bandas20m[0]+'.tif'

            RGB_TC('L2A','R20m',pathTmp+dirI,tile,pathLatest)
            RGB(r,g,b,tile,pathLatest)


            escribeDatos(pathLatest,tile,archivo,dia,hora)

        else:
            continue


os.system('rm -r '+pathTmp+'*')
os.system('rm -r '+pathL2A+'*')