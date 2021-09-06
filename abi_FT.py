#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 18:18:33 2020

@author: urielm
"""

from osgeo import gdal,osr
import numpy as np
import os
from glob import glob
#import matplotlib.pyplot as plt

def normaliza(data):
    print ('Normalizando dato...')   
    data = (data - np.nanmin(data))*255/(np.nanmax(data)-np.nanmin(data))    
    return data

def rebin(a, shape):
    sh = shape[0],a.shape[0]//shape[0],shape[1],a.shape[1]//shape[1]
    return a.reshape(sh).mean(-1).mean(1)

def compuestoRGB(r,g,b,entero):
    print ('Creando compuesto RGB...') 
    if entero == True:
        rgb = (np.dstack((r,g,b))).astype('uint8') 
    else:
        rgb = (np.dstack((r,g,b)))
    return rgb

def creaTiff(data, ds, nombre):
    print ('Creando tif...')   
    
    geotransform = ds.GetGeoTransform()
    
    # Parametros para la creacion del TIFF por medio de GDAL
    nx = data.shape[1]
    ny = abs(data.shape[0])
    dst_ds = gdal.GetDriverByName('GTiff').Create(nombre+'.tif', nx, ny, 1, gdal.GDT_Float32)
    
    # Aplica la geotransformacion y la proyección
    dst_ds.SetGeoTransform(geotransform)    # Coordenadas especificas
    srs = osr.SpatialReference()            # Establece el ensamble
    srs.ImportFromWkt(ds.GetProjectionRef())
    dst_ds.SetProjection(srs.ExportToWkt()) # Exporta el sistema de coordenadas
    dst_ds.GetRasterBand(1).WriteArray(data) # Escribe la banda al raster
    dst_ds.FlushCache()                     # Escribe en el disco
    
    dst_ds = None

def extrae(path):
    ds = gdal.Open(path)
    data = ds.ReadAsArray()
    
    return ds,data

def extraeArchivo(path,banda,region):

    if region == "conus":
    	archivos = glob(path+'*'+banda+'*')
    elif region == "fd":
        archivos = glob(path+"*"+banda+"*gs*")
    archivos.sort()
    
    archivo = archivos[-1]
    
    salida1 = archivo.split('/')[-1].split('.')[-2].split('-')[-1].split('_')
    salida1[0] = 'FT'
    salida1 = '_'.join(map(str,salida1))
    
    salida2 = archivo.split('/')[-1].split('.')[-2].split('-')
    salida2[2] = salida1    
    salida2.pop(1)
    salida2 = '-'.join(map(str,salida2))
    
    salida3 = archivo.split('/')[-1].split('.')
    salida3[-2] = salida2
    
    salida = '.'.join(map(str,salida3))
    
    return archivo,salida
       


def ftABI(r,g,b,rango):

    rmask = r
    rmask = np.where(rmask == -1,np.nan,1)
        
    r = np.where(r <= rango[0] ,rango[0],r)
    r = np.where(r >= rango[1],rango[1],r)
    
    g = np.where(g <= 0 ,0,g)
    g = np.where(g >= 1 ,1,g)
    
    b = np.where(b <= 0 ,0,b)
    b = np.where(b >= 0.75 ,0.75,b)

    r = normaliza(r).astype('uint8') 
    #r = rescala(r,0,130).astype('uint8') 
    g = normaliza(g).astype('uint8') 
    b = normaliza(b).astype('uint8') 
        
    r = r*rmask
    g = g*rmask
    b = b*rmask   
        
    print(rmask)
    print(r)
    print(g)
    print(b)
   
    return r,g,b,rmask

def reproyecta(path,banda):
    os.system('gdalwarp -t_srs EPSG:4326 '+path+' '+banda+'_geo.tif')

def recorta(banda,cuadrante):    
    xmin = cuadrante[0]
    xmax = cuadrante[1]
    ymin = cuadrante[2]
    ymax = cuadrante[3]
    
    os.system('gdal_translate -projWin '+str(xmin)+' '+str(ymax)+' '+str(xmax)+' '+str(ymin)+' '+banda+'_geo.tif '+banda+'_rec.tif')

def borra():
    tempRGB = ('R','G','B','C0')    
    for i in tempRGB:
        temp = glob('./'+i+'*.tif')
        for j in temp:
            os.remove(j)    
        
def abiFT(pathInput,pathOutput,cuadrante,shape,region):
        
    print('Extrayendo...') 
    b7,salida7 = extraeArchivo(pathInput,'C07',region)
    b6,salida6 = extraeArchivo(pathInput,'C06',region)
    b5,salida5 = extraeArchivo(pathInput,'C05',region)
    
    print('Remuestreando B5...')
    ds5,b = extrae(b5)
    ds7,r = extrae(b7)
    b = rebin(b,shape)
    creaTiff(b,ds7,'C05_rem')
    
    print('Reproyectando...')
    reproyecta(b7,'C07')
    reproyecta(b6,'C06')
    reproyecta('C05_rem.tif','C05')
    
    print('Recortando...')
    recorta('C07',cuadrante)
    recorta('C06',cuadrante)
    recorta('C05',cuadrante)
    
    print('Obteniendo FT...')
    ds7,r = extrae('C07_rec.tif')
    ds6,g = extrae('C06_rec.tif')
    ds5,b = extrae('C05_rec.tif')
    print(r.shape)
    print(g.shape)
    print(b.shape)
    #b = rebin(b,[r.shape[1],r.shape[0]])
    r,g,b,rmask = ftABI(r,g,b,(300,325))
    
    print('Creando GTiff...')
    creaTiff(r,ds7,'R')
    creaTiff(g,ds7,'G')
    creaTiff(b,ds7,'B')
    
    print('Compuesto RGB...')    
    os.system('gdal_merge.py -separate -co PHOTOMETRIC=RGB -o '+pathOutput+salida6[:-7]+".tif"+' R.tif G.tif B.tif')    
    #os.system('cp '+pathOutput+salida6+' /data2/tmp/latest/')
    #os.system('mv /data2/tmp/latest/'+salida6+' /data2/tmp/latest/abi_FT_latest.tif')   
 
    borra()
    

pathInput = '/data/goes16/abi/l2/geotiff/cmi/conus/'
pathOutput = '/data/goes16/abi/vistas/fire/conus/'
cuadrante_conus = (-118,-85,15,33.5)
shape_conus = [1500,2500]
abiFT(pathInput,pathOutput,cuadrante_conus,shape_conus,"conus")

pathInput_fires = "/data/goes16/abi/l2/geotiff/cmi/fd/"
pathOutput_fires = "/data/goes16/abi/vistas/fire/mexico_caribe/"
#cuadrante_fires = (-117.6,-58.5,6.5,33.6)
cuadrante_fires_ext = (-118,-58,6,34)
#cuadrante_a1 = (-129.791797,-50.19895,0.794,38.381128)
shape_fd = [5424,5424]
abiFT(pathInput_fires,pathOutput_fires,cuadrante_fires_ext,shape_fd,"fd")
 
