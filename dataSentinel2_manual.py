#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 11:12:47 2019
@author: urielm
"""

from pyproj import Proj, transform
from time import strftime,gmtime
import requests
#from osgeo import gdal
#import cartopy.crs as crrs
import os

def coordenadasVentana(x,y,offset):
    print ('Obteniendo coordenadas ventana...')    

    # Obtiene las coordenadas extremas de la ventana de acuerdo al offset
    urlon= x + offset
    lllon = x - offset        
      
    urlat = y + offset
    lllat = y - offset
    
    coorVentana = [lllon,urlat,urlon,lllat]    
    return coorVentana

def coorVentanaSentinelHub(x,y,offset):
    km = 111.12
    offset = offset*km*1000
    
    p1 = Proj(init='epsg:4326')
    p2 = Proj(init='epsg:3857')
    
    coorCent = transform(p1,p2,x,y)
    
    coorVentanaProj = coordenadasVentana(coorCent[0],coorCent[1],offset)
    
    return coorVentanaProj

def borraJPG(RGB):
    os.system('rm /home/urielm/webApp_ReporteSatelital/data_Sentinel2/'+RGB+'/*')

def borraTodo():
    borraJPG('TC')
    borraJPG('SWIR')
    

def extraeWMS(x,y,offset,LAYERS,salida,path,RGB):

    coorVentana = coorVentanaSentinelHub(x,y,offset)    
    
    BBOX = str(coorVentana[0])+'%2C'+str(coorVentana[3])+'%2C'+str(coorVentana[2])+'%2C'+str(coorVentana[1])
    print(BBOX)
    TIME = strftime("%Y-%m-%d", gmtime())
    #LAYERS = '1-NATURAL-COLOR,DATE'
    MAXCC = '100'
#https://services.sentinel-hub.com/ogc/wms/eadcc3e9-e764-4af4-9d3a-e191528a5262?SERVICE=WMS&REQUEST=GetMap&MAXCC=20&LAYERS=1-NATURAL-COLOR,DATE&CLOUDCORRECTION=none&EVALSOURCE=S2&TEMPORAL=false&WIDTH=1840&HEIGHT=869&ATMFILTER=ATMCOR&FORMAT=image/jpeg&NICENAME=Sentinel-2+image+on+2019-11-20.jpg&TIME=2015-01-01/2019-11-20&BBOX=-11239607,2235630,-10961376,2368477
    if LAYERS != '1_TRUE_COLOR%2CDATE':
        #url = 'https://services.sentinel-hub.com/ogc/wms/eadcc3e9-e764-4af4-9d3a-e191528a5262?SERVICE=WMS&REQUEST=GetMap&MAXCC='+MAXCC+'&LAYERS='+LAYERS+'&EVALSOURCE=S2&WIDTH=1000&HEIGHT=1000&ATMFILTER=ATMCOR&FORMAT=image/jpeg&NICENAME=Sentinel-2+image+on+2019-01-30.jpg&TIME=2018-07-01/'+TIME+'&BBOX='+BBOX+'&PREVIEW=3&EVALSCRIPT=cmV0dXJuIFtCMTIqMi41LEI4QSoyLjUsQjAzKjIuNV0%3D'	
        #url = 'https://services.sentinel-hub.com/ogc/wms/eadcc3e9-e764-4af4-9d3a-e191528a5262?SERVICE=WMS&REQUEST=GetMap&MAXCC='+MAXCC+'&LAYERS='+LAYERS+'&CLOUDCORRECTION=none&EVALSOURCE=S2&TEMPORAL=false&WIDTH=1000&HEIGHT=1000&ATMFILTER=ATMCOR&FORMAT=image/jpeg&NICENAME=Sentinel-2+image+on+'+TIME+'.jpg&TIME=2015-01-01/'+TIME+'&BBOX='+BBOX
        url = 'https://services.sentinel-hub.com/ogc/wms/26fc2e12-219a-42eb-9dde-f9f0287a7823?version=1.1.1&service=WMS&request=GetMap&format=image%2Fjpeg&crs=EPSG%3A3857&layers='+LAYERS+'&bbox='+BBOX+'&time=2019-10-01T00%3A00%3A00.000Z%2F'+TIME+'T23%3A59%3A59.999Z&width=1000&height=1000&showlogo=true&transparent=true&maxcc='+MAXCC+'&nicename=Sentinel-2%20L2A%20image%20on%20'+TIME+'.jpg&bgcolor=000000&evalsource=S2L2A'

    elif LAYERS ==  '1_TRUE_COLOR%2CDATE':
        #url = 'https://services.sentinel-hub.com/ogc/wms/b7b5e3ef-5a40-4e2a-9fd3-75ca2b81cb32?SERVICE=WMS&REQUEST=GetMap&MAXCC='+MAXCC+'&LAYERS='+LAYERS+'&EVALSOURCE=S2&WIDTH=1000&HEIGHT=1000&ATMFILTER=ATMCOR&FORMAT=image/jpeg&NICENAME=Sentinel-2+image+on+2019-01-30.jpg&TIME=2018-07-01/'+TIME+'&BBOX='+BBOX	
        #url = 'https://services.sentinel-hub.com/ogc/wms/eadcc3e9-e764-4af4-9d3a-e191528a5262?SERVICE=WMS&REQUEST=GetMap&MAXCC='+MAXCC+'&LAYERS='+LAYERS+'&CLOUDCORRECTION=none&EVALSOURCE=S2&TEMPORAL=false&WIDTH=1000&HEIGHT=1000&ATMFILTER=ATMCOR&FORMAT=image/jpeg&NICENAME=Sentinel-2+image+on+'+TIME+'.jpg&TIME=2015-01-01/'+TIME+'&BBOX='+BBOX
        url = 'https://services.sentinel-hub.com/ogc/wms/26fc2e12-219a-42eb-9dde-f9f0287a7823?version=1.1.1&service=WMS&request=GetMap&format=image%2Fjpeg&crs=EPSG%3A3857&layers='+LAYERS+'&bbox='+BBOX+'&time=2019-10-01T00%3A00%3A00.000Z%2F'+TIME+'T23%3A59%3A59.999Z&width=1000&height=1000&showlogo=true&transparent=true&maxcc='+MAXCC+'&nicename=Sentinel-2%20L2A%20image%20on%20'+TIME+'.jpg&bgcolor=000000&evalsource=S2L2A'

    r = requests.get(url)    
    code = open(path+'/'+salida+str(x)+"_"+str(y)+".jpg", "wb")
    code.write(r.content)
    code = None

    return salida+str(x)+"_"+str(y)+".jpg"

'''
lat = 19.02
lon = -98.63
offset = 0.05
path = '.'

extraeWMS(lon,lat,offset,'1_TRUE_COLOR%2CDATE','TC_',path,'TC')
extraeWMS(lon,lat,offset,'2_FALSE_COLOR%2CDATE','FC_',path,'FC')
extraeWMS(lon,lat,offset,'6_SWIR%2CDATE','SWIR_',path,'SWIR')
extraeWMS(lon,lat,offset,'3_NDVI%2CDATE','NDVI_',path,'NDVI')
'''
#borraTodo()
