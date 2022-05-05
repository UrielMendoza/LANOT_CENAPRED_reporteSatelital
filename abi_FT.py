#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 18:18:33 2020

@author: urielm
"""

from datetime import datetime
#from abi_TC import convierteVista
from osgeo import gdal,osr
import numpy as np
import os
from glob import glob
from PIL import Image, ImageDraw
import aggdraw
#import matplotlib.pyplot as plt


def draw_text(im_in,x, y, text, align, bw=5):
    draw = aggdraw.Draw(im_in)
    p = aggdraw.Pen("white", 0.5)
    b = aggdraw.Brush((0,0,0), 100)
    white = (255, 255, 255)
    font = aggdraw.Font(white, "/usr/share/fonts/truetype/ttf-bitstream-vera/VeraMono.ttf", 25)

    p = aggdraw.Pen("white", 0.5)
    b = aggdraw.Brush((0,0,0), 100)
    title_sz =  draw.textsize(text, font)
    if align == 1:
        x -= title_sz[0]/2
    elif align == 2:
        x -= title_sz[0]
    draw.rectangle((x-bw, y, x+title_sz[0]+bw, y+title_sz[1]), b, b) 
    draw.text((x, y), text, font)
    draw.flush()

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
    dst_ds = gdal.GetDriverByName('GTiff').Create(nombre+'.tif', nx, ny, 1, gdal.GDT_Byte)
    
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
        archivos = glob(path+"*"+banda+"*")
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
    
    print(archivo.split('/')[-1].split('_'))
    fechastr =  archivo.split('/')[-1].split('_')[0].split('-')[1]
    #fecha = datetime.strptime('s%Y%J%H%M%S',fechastr)

    return archivo,salida,fechastr
       


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

def borra(pathTmp):
    #tempRGB = ('R','G','B','C0')    
    #for i in tempRGB:
    #    temp = glob(pathTmp+i+'*.tif')
    #    for j in temp:
    #        os.remove(j)  
    os.system('rm '+pathTmp+'*')    
        
def abiFT(pathInput,pathTmp,pathOutput,cuadrante,shape,region,regionrec):
        
    print('Extrayendo...') 
    b7,salida7,fecha = extraeArchivo(pathInput,'C07',region)
    b6,salida6,fecha = extraeArchivo(pathInput,'C06',region)
    b5,salida5,fecha = extraeArchivo(pathInput,'C05',region)
    
    print('Remuestreando B5...')
    ds5,b = extrae(b5)
    ds7,r = extrae(b7)
    b = rebin(b,shape)
    creaTiff(b,ds7,pathTmp+'C05_rem')
    
    print('Reproyectando...')
    reproyecta(b7,pathTmp+'C07')
    reproyecta(b6,pathTmp+'C06')
    reproyecta(pathTmp+'C05_rem.tif',pathTmp+'C05')
    
    print('Recortando...')
    recorta(pathTmp+'C07',cuadrante)
    recorta(pathTmp+'C06',cuadrante)
    recorta(pathTmp+'C05',cuadrante)
    
    print('Obteniendo FT...')
    ds7,r = extrae(pathTmp+'C07_rec.tif')
    ds6,g = extrae(pathTmp+'C06_rec.tif')
    ds5,b = extrae(pathTmp+'C05_rec.tif')
    print(r.shape)
    print(g.shape)
    print(b.shape)
    #b = rebin(b,[r.shape[1],r.shape[0]])
    r,g,b,rmask = ftABI(r,g,b,(300,325))
    
    print('Creando GTiff...')
    creaTiff(r,ds7,pathTmp+'R')
    creaTiff(g,ds7,pathTmp+'G')
    creaTiff(b,ds7,pathTmp+'B')
    
    #fechaName = fecha.strptime('%Y.%m%d.%H%M')
    name = 'goes16.abi-'+fecha+'-fire-'+regionrec+'.tif'
    namepng = 'goes16.abi-'+fecha+'-fire-'+regionrec+'.png'
    namejpg = 'goes16.abi-'+fecha+'-fire-'+regionrec+'.jpg'

    print('Compuesto RGB...')    
    os.system('gdal_merge.py -separate -co PHOTOMETRIC=RGB -o '+pathTmp+name+' '+pathTmp+'R.tif '+pathTmp+'G.tif '+pathTmp+'B.tif')    
    #os.system('gdal_translate '+pathTmp+name+' '+pathTmp+namepng)
    os.system('gdal_translate '+pathTmp+name+' '+pathTmp+namejpg)

    pathLanot = '/usr/local/share/lanot/'
    im_in = Image.open(pathTmp+namejpg)
    height = 1200
    width = int(height * im_in.width / im_in.height)
    im_in = im_in.resize((width, height)).convert('RGB')
    logo = Image.open(pathLanot + '/logos/lanot_negro_sn.jpg')
    w = 200
    h = int(w * logo.height / logo.width)
    logo = logo.resize((w, h))
    im_in.paste(logo, (10, 10))

    print(fecha)
    fechaVista = datetime.strptime(fecha,'%Y.%m%d.%H%M')
    fechaStr = 'GOES-16/ABI fire temperature '+fechaVista.strftime('%Y/%m/%d %H:%MZ')
    draw_text(im_in, im_in.width-15, im_in.height - 40, fechaStr, 2)
    im_in.save(pathTmp+namejpg)  


    os.system('cp '+pathTmp+namejpg+' '+pathOutput)
    #os.system('cp '+pathOutput+salida6+' /data2/tmp/latest/')
    #os.system('mv /data2/tmp/latest/'+salida6+' /data2/tmp/latest/abi_FT_latest.tif')   
 
    borra(pathTmp)

    return namejpg
    

def convierteVista(pathInput,pathOutput,cuadrante):
    xmin = cuadrante[0]
    xmax = cuadrante[1]
    ymin = cuadrante[2]
    ymax = cuadrante[3] 
    
    os.system("gdal_translate -a_ullr "+str(xmin)+' '+str(ymax)+' '+str(xmax)+' '+str(ymin)+" -a_srs EPSG:4326 "+pathInput+" "+pathOutput)

#pathInput = '/data/goes16/abi/l2/geotiff/cmi/conus/'
#pathOutput = '/data/goes16/abi/vistas/fire/conus/'
#cuadrante_conus = (-118,-85,15,33.5)
#shape_conus = [1500,2500]
#abiFT(pathInput,pathOutput,cuadrante_conus,shape_conus,"conus")

pathTmp = '/home/lanotadm/data/tmp/abi_FT_latest/'
pathOutput = '/home/lanotadm/data/latest/'

pathInput_a1 = "/data/goes16/abi/l2/geotiff/cmi/fd/"
pathOutput_a1 = "/dataservice/goes16/abi/vistas/fire/"
#cuadrante_fires = (-117.6,-58.5,6.5,33.6)
cuadrante_a1 = (-129.791797,-50.19895,0.794,38.381128)
#cuadrante_a1 = (-129.791797,-50.19895,0.794,38.381128)
shape_fd = [5424,5424]
name = abiFT(pathInput_a1,pathTmp,pathOutput_a1,cuadrante_a1,shape_fd,"fd",'a1')
convierteVista(pathOutput_a1+name,pathOutput+"abi_FT_a1_latest.tif",cuadrante_a1)


pathInput_fires = "/data/goes16/abi/l2/geotiff/cmi/fd/"
pathOutput_fires = "/dataservice/goes16/abi/vistas/fire/"
#cuadrante_fires = (-117.6,-58.5,6.5,33.6)
cuadrante_fires_ext = (-118,-58,6,34)
#cuadrante_a1 = (-129.791797,-50.19895,0.794,38.381128)
shape_fd = [5424,5424]
name = abiFT(pathInput_fires,pathTmp,pathOutput_fires,cuadrante_fires_ext,shape_fd,"fd",'fires')
#convierteVista(pathOutput_fires+name,pathOutput+"abi_FT_fires_latest.tif",cuadrante_fires_ext)
 
