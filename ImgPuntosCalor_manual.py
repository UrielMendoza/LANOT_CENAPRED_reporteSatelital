#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 13:29:32 2019

@author: lanot
"""
import matplotlib
matplotlib.use('Agg')
import dataSentinel2_manual

#import matplotlib.pyplot as plt
#import cartopy.crs as crrs
#from osgeo import gdal

import ensamble_manual

import os

from datetime import datetime

from glob import glob

def coordenadasVentana(x,y,offset):
    print ('Obteniendo coordenadas ventana...')    

    # Obtiene las coordenadas extremas de la ventana de acuerdo al offset
    urlon= x + offset
    lllon = x - offset        
      
    urlat = y + offset
    lllat = y - offset
    
    coorVentana = [lllon,urlat,urlon,lllat]    
    return coorVentana

def recorta(x,y,offset,pathInput,pathOutput,salida):    
    xmin = offset[0]
    xmax = offset[2]
    ymin = offset[3]
    ymax = offset[1]
    
    os.system('gdal_translate -projWin '+str(xmin)+' '+str(ymax)+' '+str(xmax)+' '+str(ymin)+' '+pathInput+salida+'.tif '+pathOutput+salida+'_'+str(x)+'_'+str(y)+'.png')

    return pathOutput+salida+'_'+str(x)+'_'+str(y)+'.png'

def fechaG16(pathInput):
    archivos = glob(pathInput+'*')
    archivos.sort()
    
    archivo = archivos[-1]
    
    dia = archivo.split('/')[-1].split('.')[:3]
    dia = '-'.join(map(str,dia))
    hora = archivo.split('/')[-1].split('.')[3:5]
    hora = ':'.join(map(str,hora))
 
    fecha = dia+'T'+hora+'Z'

    return fecha

def fechaNOAA20(pathInput):
    archivos = glob(pathInput+'*')
    archivos.sort()
    
    archivo = archivos[-1]
    
    dia = archivo.split('/')[-1].split('_')[1].split('.')[-1]
    dia = dia[1:5]+'-'+dia[5:7]+'-'+dia[7:]
    hora = archivo.split('/')[-1].split('_')[3].split('.')[0]
    hora = hora[1:3]+':'+hora[3:5]
    
    fecha = dia+'T'+hora+'Z'

    return fecha
'''
def plotRGB(rgb,coorVentana,x,y,salida):
    print ('Ploteando datos RGB...')   
    
    salida = '/home/incendios/IncendiosDinamicos/output/'+salida
    
    plt.figure(figsize=(10,10))
    ax = plt.axes(projection=crrs.PlateCarree())
    ax.coastlines(resolution='50m',color='w')
    #ax.gridlines(linestyle='--')
    ax.set_extent([coorVentana[0],coorVentana[2],coorVentana[3],coorVentana[1]])
    plt.imshow(rgb,extent=[coorVentana[0],coorVentana[2],coorVentana[3],coorVentana[1]])
    plt.plot(x,y,'c+',markersize = 20)
        
    imagen = salida+str(x)+'_'+str(y)+'.png'
    
    plt.savefig(imagen,dpi=300,bbox_inches='tight', pad_inches=0)
    
    rgb = None  
    
    return imagen
'''
def manual(x,y):
	#borra()
    
    pathInput = '/home/urielm/webApp_ReporteSatelital/latest/'
    pathOutput = '/home/urielm/webApp_ReporteSatelital/'
    
    pathFechaG16 = '/home/urielm/webApp_ReporteSatelital/latest/fechas/GOES16/'
    pathFechaNOAA20 = '/home/urielm/webApp_ReporteSatelital/latest/fechas/NOAA20/'
    
    pathGOES16 = pathOutput+'data_GOES16/'
    pathNOAA20 = pathOutput+'data_NOAA20/'
    pathSentinel2 = pathOutput+'data_Sentinel2/'
    
    print ("\nProcesando Coordenada: ",x,',',y)
    x = float(x)
    y = float(y)

    offsetGOES16 = 1
    offsetNOAA20 = 0.5
    offsetSentinel2 = 0.1

    offsetGOES16 = coordenadasVentana(x,y,offsetGOES16)
    offsetNOAA20 = coordenadasVentana(x,y,offsetNOAA20)
    #offsetSentinel2 = coordenadasVentana(x,y,offsetSentinel2)

    # AQUI DEBERIA ESTAR SENTINEL HUB :(
    #Sen2_TC_imagen = pathSentinel2+dataSentinel2_manual.extraeWMS(x,y,offsetSentinel2,'1_TRUE_COLOR%2CDATE','TC_',pathSentinel2,'TC')
    #Sen2_SWIR_imagen = pathSentinel2+dataSentinel2_manual.extraeWMS(x,y,offsetSentinel2,'6_SWIR%2CDATE','SWIR_',pathSentinel2,'SWIR')
    Sen2_TC_imagen = '/home/urielm/webApp_ReporteSatelital/static/latest.png'
    Sen2_SWIR_imagen = '/home/urielm/webApp_ReporteSatelital/static/latest.png'
    G16_TC_imagen = recorta(x,y,offsetGOES16,pathInput,pathGOES16,'abi_TC_a1_latest')
    G16_FT_imagen = recorta(x,y,offsetGOES16,pathInput,pathGOES16,'abi_FT_latest')
    # AQUI TAMBIENE STA MAL TODO EN FT DE VIIRS
    NOAA20_TC_imagen = recorta(x,y,offsetNOAA20,pathInput,pathNOAA20,'viirs_TC_latest')
    NOAA20_FT_imagen = recorta(x,y,offsetNOAA20,pathInput,pathNOAA20,'latest.png')
    #NOAA20_TC_imagen = recorta(x,y,offsetNOAA20,pathInput,pathNOAA20,'viirs_TC_latest')
    #NOAA20_FT_imagen = recorta(x,y,offsetNOAA20,pathInput,pathNOAA20,'viirs_FT_latest')  
    
    fecha_G16 = fechaG16(pathFechaG16)     
    fecha_NOAA20 = fechaNOAA20(pathFechaNOAA20)

	#QUITAR ESTO
    tmpPC = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    logo_path = 'logo.png'
    logoC_path = 'logo_CENAPRED.png'
    ubiMun_path = 'ubicacion_muni_'+str(x)+'_'+str(y)+'.png'
    ubiEnt_path = 'ubicacion_edo_'+str(x)+'_'+str(y)+'.png'
    imgF = ensamble_manual.ensambleSat(x,y,G16_TC_imagen,G16_FT_imagen,NOAA20_TC_imagen,NOAA20_FT_imagen,Sen2_TC_imagen,Sen2_SWIR_imagen,ubiMun_path,ubiEnt_path,logo_path,logoC_path,tmpPC,fecha_G16,fecha_NOAA20)

	#infoArchivo.write('\n'+str(x)+','+str(y)+','+str(tmpPC))
	#infoArchivo.close()

    os.remove(G16_TC_imagen)
    os.remove(G16_FT_imagen)
    os.remove(G16_TC_imagen+'.aux.xml')
    os.remove(G16_FT_imagen+'.aux.xml')
    
    os.remove(NOAA20_TC_imagen)
    #os.remove(NOAA20_FT_imagen)
    os.remove(NOAA20_TC_imagen+'.aux.xml')
    #os.remove(NOAA20_FT_imagen+'.aux.xml')
    
    #os.remove(Sen2_TC_imagen)    
    #os.remove(Sen2_SWIR_imagen)
    os.remove('ubicacion_muni_'+str(x)+'_'+str(y)+'.png')
    os.remove('ubicacion_edo_'+str(x)+'_'+str(y)+'.png')
	  
	#os.system('rm /home/incendios/IncendiosDinamicos/output/*')
	
    return imgF

#lon = -100.2
#lat = 20.2

#manual(lon,lat)
