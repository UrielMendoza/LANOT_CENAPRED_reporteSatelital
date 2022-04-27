#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 12:52:43 2020

@author: urielm
"""

from osgeo import gdal,osr
import numpy as np
import os
from glob import glob

def revisaFecha(path):
    archivos = glob(path+'*goes-16.rgb*')
    archivos.sort()
    ultimo = archivos[-1]
    print(ultimo)
    diaU = '-'.join(map(str,ultimo.split('/')[-1].split('.')[:3]))
    horaU = ':'.join(map(str,ultimo.split('/')[-1].split('.')[3:5]))
    print(diaU)
    print(horaU)

    return ultimo,diaU,horaU

def reproyecta(path,tmp):
    os.system('gdalwarp -t_srs EPSG:4326 '+path+" /var/tmp/"+tmp+".tif")
    
def recorta(pathOutput,cuadrante,tmp,latest):    
    xmin = cuadrante[0]
    xmax = cuadrante[1]
    ymin = cuadrante[2]
    ymax = cuadrante[3]
    
    os.system('gdal_translate -projWin '+str(xmin)+' '+str(ymax)+' '+str(xmax)+' '+str(ymin)+" "+tmp+" "+pathOutput+latest+".tif")

def borra():
    os.remove('/var/tmp/tmp_geo.tif')    
    os.remove("/var/tmp/tmp_geo_fd.tif")

def escribeDatos(pathOutput,sector,ultimo,dia,hora):
   file = open(pathOutput+'/'+sector+"_date_latest.txt","w")
   file.write(ultimo+","+dia+","+hora)
   file.close()

def convierteVista(pathInput,pathOutput,cuadrante):
   xmin = cuadrante[0]
   xmax = cuadrante[1]
   ymin = cuadrante[2]
   ymax = cuadrante[3] 
   
   os.system("gdal_translate -a_ullr "+str(xmin)+' '+str(ymax)+' '+str(xmax)+' '+str(ymin)+" -a_srs EPSG:4326 "+pathInput+" "+pathOutput)

def abiTC(pathInput,pathInput2,pathOutput):
    cuadrante_mex = (-118,-85,15,33.5)
    cuadrante_fires = (-117.6,-58.5,6.5,33.6)
    cuadrante_fires_ext = (-118,-58,6,34)
    cuadrante_a1 = (-129.791797,-50.19895,0.794,38.381128)

    ultimo,diaU,horaU = revisaFecha(pathInput+"/conus/")
    ultimoFD,diaFD,horaFD = revisaFecha(pathInput+"/fd/")
    ultimoA1,diaA1,horaA1 = revisaFecha(pathInput+"/a1/")

    escribeDatos(pathOutput,"conus",ultimo,diaU,horaU)
    escribeDatos(pathOutput,"fd",ultimoFD,diaFD,horaFD)

    #reproyecta(pathInput2+"rgbconus/tmp.tif","tmp_geo")
    #reproyecta(pathInput2+"rgb/tmp.tif","tmp_geo_fd")

    #recorta(pathOutput,cuadrante_mex,"/var/tmp/tmp_geo.tif","abi_TC_latest")
    #recorta(pathOutput,cuadrante_fires,"/var/tmp/tmp_geo_fd.tif","abi_TC_fires_latest")

    convierteVista(ultimoA1,pathOutput+"abi_TC_a1_latest.tif",cuadrante_a1)
    recorta(pathOutput,cuadrante_fires_ext,pathOutput+"abi_TC_a1_latest.tif","abi_FD_TC_fires_latest")

    #borra()
    
pathInput = "/var/www/html/goes16/abi/vistas/rgb"
pathTmp = "/home/lanotadm/data/tmp"
pathOutput = '/home/lanotadm/data/latest'

abiTC(pathInput,pathTmp,pathOutput)
